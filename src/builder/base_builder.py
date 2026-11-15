from typing import Any, Dict


class BaseBuilder:
    def __init__(self, resource_type: str):
        self.data: Dict[str, Any] = {"resourceType": resource_type}

    @staticmethod
    def _titik(wadah: Any, segs: list):
        """Telusuri jalur `a/b/0/c`, buat objek antara, dan kembalikan (induk, kunci akhir)."""
        cur = wadah
        for i, seg in enumerate(segs[:-1]):
            kunci: Any = int(seg) if seg.lstrip("-").isdigit() else seg
            if isinstance(cur, list):
                while len(cur) <= kunci:
                    cur.append({})
                cur = cur[kunci]
                continue
            if kunci not in cur or not isinstance(cur[kunci], (dict, list)):
                cur[kunci] = [] if segs[i + 1].lstrip("-").isdigit() else {}
            cur = cur[kunci]
        akhir = segs[-1]
        return cur, (int(akhir) if akhir.lstrip("-").isdigit() else akhir)

    def _set(self, key: str, value: Any) -> "BaseBuilder":
        """`set('period/start', …)` menulis period.start, bukan kunci literal "period/start"."""
        if value is not None and value != "" and value != [] and value != {}:
            induk, akhir = self._titik(self.data, key.split("/"))
            induk[akhir] = value
        return self

    def _push(self, key: str, value: Any) -> "BaseBuilder":
        induk, akhir = self._titik(self.data, key.split("/"))
        if not isinstance(induk.get(akhir), list):
            induk[akhir] = []
        induk[akhir].append(value)
        return self

    def _append(self, key: str, value: Any) -> "BaseBuilder":
        return self._push(key, value)

    def _auto_prefix(self, ref: str, resource_type: str) -> str:
        """Auto-prefix bare reference with resource type if no urn:/http(s):// or / present."""
        if not ref.startswith(("urn:", "http://", "https://")) and "/" not in ref:
            return f"{resource_type}/{ref}"
        return ref

    def _ref(self, ref: str, resource_type: str, display: str = None) -> Dict[str, Any]:
        """Build a Reference dict with auto-prefix."""
        result: Dict[str, Any] = {"reference": self._auto_prefix(ref, resource_type)}
        if display:
            result["display"] = display
        return result

    def build(self) -> Dict[str, Any]:
        return {k: v for k, v in self.data.items() if v not in (None, "", [], {})}

    def to_array(self) -> Dict[str, Any]:
        return self.build()
