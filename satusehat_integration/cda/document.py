"""HL7 CDA R2 ClinicalDocument: parse, inspect, and build the minimum a record exchange needs.

Scope is deliberate. CDA R2 is hundreds of pages of optional structure; what gets used is the header
(who, what, when, where, signed by whom) and the sections with narrative text. Those are modelled.
Everything else stays in the ElementTree and is written back on :meth:`Document.to_xml`, so a document
containing structures this class does not understand survives a round trip instead of being truncated.

The HL7 CDA R2 schemas are licensed; this module implements the structural rules from the
specification and does not redistribute them.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime

from .patient import PatientRole
from .section import LOINC, Section

CDA_NS = "urn:hl7-org:v3"
NS = "{urn:hl7-org:v3}"

ET.register_namespace("", CDA_NS)


class CdaError(ValueError):
    """Raised for input that is not an XML ClinicalDocument."""


def _q(tag: str) -> str:
    return NS + tag


class Document:
    def __init__(self, root: ET.Element):
        self._root = root

    # ------------------------------------------------------------------ parsing

    @classmethod
    def parse(cls, xml: str) -> "Document":
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as exc:
            raise CdaError("XML CDA tidak sah.") from exc
        name = root.tag.split("}")[-1]
        if name != "ClinicalDocument":
            raise CdaError(f"Akar dokumen adalah {name}, bukan ClinicalDocument.")
        return cls(root)

    # ------------------------------------------------------------------ header

    def title(self) -> str:
        return self._text(self._root.find(_q("title"))) 

    def document_id(self) -> str:
        node = self._root.find(_q("id"))
        if node is None:
            return ""
        root = node.get("root", "")
        ext = node.get("extension", "")
        return f"{root}|{ext}" if ext else root

    def type_code(self) -> str:
        node = self._root.find(_q("code"))
        return node.get("code", "") if node is not None else ""

    def effective_time(self) -> str:
        node = self._root.find(_q("effectiveTime"))
        return node.get("value", "") if node is not None else ""

    def custodian(self) -> str:
        return self._text(self._root.find(f"{_q('custodian')}//{_q('name')}"))

    def authors(self) -> list[str]:
        out: list[str] = []
        for author in self._root.findall(_q("author")):
            given = self._text(author.find(f".//{_q('name')}/{_q('given')}"))
            family = self._text(author.find(f".//{_q('name')}/{_q('family')}"))
            name = f"{given} {family}".strip()
            if not name:
                name = self._text(author.find(f".//{_q('softwareName')}"))
            if name:
                out.append(name)
        return out

    def patient(self) -> PatientRole:
        role = self._root.find(f"{_q('recordTarget')}/{_q('patientRole')}")
        if role is None:
            return PatientRole()
        identifiers = [
            {"root": node.get("root", ""), "extension": node.get("extension", "")}
            for node in role.findall(_q("id"))
        ]
        names = []
        for name in role.findall(f".//{_q('name')}"):
            value = f"{self._text(name.find(_q('given')))} {self._text(name.find(_q('family')))}".strip()
            if value:
                names.append(value)
        gender = role.find(f".//{_q('administrativeGenderCode')}")
        birth = role.find(f".//{_q('birthTime')}")
        return PatientRole(
            identifiers,
            names,
            gender.get("code", "") if gender is not None else "",
            birth.get("value", "") if birth is not None else "",
        )

    # ------------------------------------------------------------------ sections

    def sections(self) -> list[Section]:
        body = self._root.find(f"{_q('component')}/{_q('structuredBody')}")
        if body is None:
            return []
        return [self._read_section(node) for node in self._sections_of(body)]

    def section(self, loinc: str) -> Section | None:
        for section in self.sections():
            hit = section.find(loinc)
            if hit is not None:
                return hit
        return None

    def section_text(self, loinc: str) -> str:
        section = self.section(loinc)
        return self.plain_text(section.text) if section else ""

    @staticmethod
    def _sections_of(parent: ET.Element) -> list[ET.Element]:
        # structuredBody wraps each section in a <component>; unwrap one level.
        return [
            node
            for comp in parent.findall(_q("component"))
            for node in comp.findall(_q("section"))
        ]

    def _read_section(self, node: ET.Element) -> Section:
        codes = {}
        for code in node.findall(_q("code")):
            system = code.get("codeSystem", "")
            value = code.get("code", "")
            if system and value:
                codes[system] = value
        text_node = node.find(_q("text"))
        return Section(
            title=self._text(node.find(_q("title"))),
            text=ET.tostring(text_node, encoding="unicode") if text_node is not None else "",
            codes=codes,
            children=[self._read_section(child) for child in self._sections_of(node)],
        )

    @staticmethod
    def plain_text(xml: str) -> str:
        """Flatten CDA narrative markup to text, keeping paragraph breaks."""
        if not xml.strip():
            return ""
        try:
            node = ET.fromstring(xml)
        except ET.ParseError:
            return xml.strip()
        parts: list[str] = []
        for element in node.iter():
            if element.tag.split("}")[-1] in ("paragraph", "item", "tr", "caption"):
                parts.append("\n")
            if element.text and element.text.strip():
                parts.append(element.text.strip())
            if element.tail and element.tail.strip():
                parts.append(element.tail.strip())
        return re.sub(r"\n{3,}", "\n\n", "".join(parts)).strip()

    @staticmethod
    def _text(node: ET.Element | None) -> str:
        if node is None:
            return ""
        return (node.text or "").strip()

    # ------------------------------------------------------------------ building

    @classmethod
    def build(cls, data: dict) -> "Document":
        """Build a minimal but structurally valid ClinicalDocument from a dict."""
        esc = _escape
        doc_id = data.get("id") or "DOC" + datetime.now().strftime("%Y%m%d%H%M%S")
        now = data.get("effectiveTime") or datetime.now().strftime("%Y%m%d%H%M%S")
        patient_root = data.get("patientIdRoot", "2.16.840.1.113883.3.3157.1003.1")
        sections = "".join(
            "<component><section>"
            + (f'<code code="{esc(s["loinc"])}" codeSystem="{LOINC}"/>' if s.get("loinc") else "")
            + f'<title>{esc(s.get("title", ""))}</title>'
            + f'<text>{s.get("text", "")}</text>'
            + "</section></component>"
            for s in data.get("sections", [])
        )
        xml = (
            f'<ClinicalDocument xmlns="{CDA_NS}">'
            '<realmCode code="ID"/>'
            '<typeId root="2.16.840.1.113883.1.3" extension="POCD_MT000040"/>'
            '<templateId root="2.16.840.1.113883.10.20.22.1.1"/>'
            f'<id root="{esc(doc_id)}"/>'
            f'<code code="{esc(data.get("code", "34133-9"))}" codeSystem="{LOINC}"'
            f' displayName="{esc(data.get("codeDisplay", "Summarization of episode note"))}"/>'
            f'<title>{esc(data.get("title", "Catatan Medis"))}</title>'
            f'<effectiveTime value="{esc(now)}"/>'
            '<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>'
            "<recordTarget><patientRole>"
            + (
                f'<id root="{esc(patient_root)}" extension="{esc(data["patientId"])}"/>'
                if data.get("patientId")
                else ""
            )
            + "<patient>"
            + (
                f'<name><family>{esc(data["patientName"])}</family></name>'
                if data.get("patientName")
                else ""
            )
            + (
                f'<administrativeGenderCode code="{esc(data["gender"])}"'
                ' codeSystem="2.16.840.1.113883.5.1"/>'
                if data.get("gender")
                else ""
            )
            + (
                f'<birthTime value="{esc(data["birthTime"])}"/>' if data.get("birthTime") else ""
            )
            + "</patient></patientRole></recordTarget>"
            f'<author><time value="{esc(now)}"/><assignedAuthor><id root="{esc(doc_id)}.AUTH"/>'
            f'<assignedPerson><name><given>{esc(data.get("author", ""))}</given></name></assignedPerson>'
            "</assignedAuthor></author>"
            "<custodian><assignedCustodian><representedCustodianOrganization>"
            f'<name>{esc(data.get("custodian", ""))}</name>'
            "</representedCustodianOrganization></assignedCustodian></custodian>"
            f"<component><structuredBody>{sections}</structuredBody></component>"
            "</ClinicalDocument>"
        )
        return cls.parse(xml)

    # ------------------------------------------------------------------ checking

    def validate(self) -> list[str]:
        """Structural check of the header rules that matter for exchange.

        An empty list means exchangeable, not clinically correct.
        """
        problems = []
        if not self.document_id():
            problems.append("ClinicalDocument/id wajib ada.")
        if not self.title():
            problems.append("ClinicalDocument/title wajib ada.")
        if not self.type_code():
            problems.append("ClinicalDocument/code wajib ada.")
        if not self.effective_time():
            problems.append("ClinicalDocument/effectiveTime wajib ada.")
        if self._root.find(_q("recordTarget")) is None:
            problems.append("recordTarget wajib ada.")
        if not self.patient().identifiers:
            problems.append("recordTarget/patientRole/id wajib ada.")
        if not self.custodian():
            problems.append("custodian wajib ada.")
        if not self.authors():
            problems.append("author wajib ada.")
        if not self.sections():
            problems.append("structuredBody wajib berisi minimal satu section.")
        return problems

    def to_xml(self) -> str:
        """The document as XML; unknown structure parsed earlier is written back unchanged."""
        return ET.tostring(self._root, encoding="unicode")


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
