"""ImagingStudy: 18 setter PHP, dengan jalur bersarang series/<i>/instance/<j>/..."""
import json
from pathlib import Path

from src.builder.imaging_study import ImagingStudyBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
DCM = "http://dicom.nema.org/resources/ontology/DCM"
SNOMED = "http://snomed.info/sct"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ImagingStudyBuilder:
    return (
        ImagingStudyBuilder()
        .set_id("img-1")
        .add_identifier("http://sys.id/ni", "NI-1500")
        .set_status("available")
        .add_modality(DCM, "CT", "Computed Tomography")
        .set_subject("Patient/1000000001")
        .set_encounter("Encounter/enc-1")
        .set_started("2026-01-05T09:00:00+07:00")
        .set_ended("2026-01-05T09:30:00+07:00")
        .set_location("Location/loc-1")
        .add_referrer("Practitioner/1000000002")
        .add_referrer("Practitioner/1000000003")
        .add_part_of("ImagingStudy/img-0")
        .add_part_of("ImagingStudy/img-00")
        .add_series("1.2.840.1.1", DCM, "CT", "Computed Tomography", "available", "Potongan toraks", 1)
        .add_series("1.2.840.2.2", DCM, "MR", "Magnetic Resonance")
        .set_series_started(1, "2026-01-05T10:00:00+07:00")
        .set_series_body_site(1, SNOMED, "51185008", "Toraks")
        .set_series_body_site(0, SNOMED, "51185008")
        .add_series_instance(1, "1.2.3.4.5", DCM, "1.2.840.10008.5.1.4.1.1.4", "MR Image Storage")
        .add_series_instance(1, "1.2.3.4.6", DCM, "1.2.840.10008.5.1.4.1.1.4", "MR Image Storage")
        .add_series_instance_number(1, 0, 5)
        .add_series_instance_number(1, 1, 6)
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("imaging_study")


def test_add_referrer_menimpa_bukan_menumpuk():
    """Dinamai 'add' tetapi R4 0..1 — kanon menimpa, dan itu ditiru."""
    referrer = isi().build()["referrer"]
    assert isinstance(referrer, dict)
    assert referrer["reference"] == "Practitioner/1000000003"


def test_series_kedua_tidak_mewarisi_started_series_pertama():
    series = isi().build()["series"]
    assert "started" not in series[0]
    assert series[1]["started"] == "2026-01-05T10:00:00+07:00"


def test_body_site_codeable_concept_sementara_modality_coding():
    series = isi().build()["series"]
    assert "coding" in series[1]["bodySite"]
    assert "coding" not in series[1]["modality"]


def test_instance_number_menempel_pada_instance_yang_benar():
    instance = isi().build()["series"][1]["instance"]
    assert [i["number"] for i in instance] == [5, 6]


def test_quirk_series_status_bukan_elemen_r4():
    assert isi().build()["series"][0]["status"] == "available"
