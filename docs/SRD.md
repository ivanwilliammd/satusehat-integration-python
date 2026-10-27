# SRD — satusehat-integration (SDK SATUSEHAT FHIR R4 · Python)

Status: v1.0 · 2026-10-27 · Pendamping: `docs/PRD-SDK-ECOSYSTEM.md` (repo PHP) + `README.md`
Versi paket terpasang: **4.14.1** (`pyproject.toml`).

Seluruh angka di dokumen ini **diukur** dari checkout ini pada 2026-10-27, bukan dari ingatan.
Bila kode berubah, perbarui dokumen ini di commit yang sama.

## 1. Ruang Lingkup

Cara kerja internal SDK: lapisan, kontrak publik, selisih nyata terhadap SDK PHP, pemetaan galat,
aturan kompatibilitas, dan hasil uji. Cara memakai SATUSEHAT ada di `README.md`.

## 2. Prinsip Arsitektur

1. **Bangun dulu, kirim kemudian.** `src/builder`, `src/datatype` tidak menyentuh jaringan. Lapisan
   pengiriman FHIR **belum ada** (lihat §5); satu-satunya jalur jaringan adalah `TerminologyClient`.
2. **Paket pip, bukan skrip.** Struktur `src/` dipasang lewat `pyproject.toml`; uji dijalankan sebagai
   paket terpasang (`uv run pytest src`), bukan dengan menyetel `PYTHONPATH` manual.
3. **Rahasia hanya dari lingkungan.** PAT/OIDC client dibaca dari argumen pemanggil.
4. **Satu perilaku, empat bahasa.** Nama kelas Python memakai `snake_case` file + `PascalCase` kelas;
   bentuk payload FHIR harus identik dengan SDK lain pada nomor rilis yang sama.

## 3. Inventaris Terukur

| Bagian | Jumlah | Cara mengukur |
|---|---|---|
| Berkas builder | 144 | `ls src/builder/*.py \| wc -l` |
| Kelas builder (tanpa berkas uji) | 140 | `grep -rhoE "^class [A-Za-z0-9_]+Builder" $(ls src/builder/*.py \| grep -v test_) \| wc -l` |
| Kelas DataType | 33 | idem pada `src/datatype/*.py` tanpa `test_` |
| Berkas terminology | 27 | `ls src/terminology/*.py \| wc -l` |
| Berkas queue | 3 | `rate_limiter.py`, `monitor.py`, `error_classifier.py` |
| Berkas uji | 5 | `find src -name "test_*.py"` |
| Fungsi uji (`def test_`) | 54 | `grep -rhoE "^\s*def test_" src --include="test_*.py" \| wc -l` |
| **Hasil pytest** | **79 lulus, 0 gagal** (0,89 s) | `uv run --with pytest --with requests --with pydantic pytest src -q` |

## 4. Kontrak Publik

- Nama paket PyPI: `satusehat-integration`; modul `src/` (lihat `[project]` di `pyproject.toml`).
- Ekspor builder: satu modul per resource (`src/builder/condition.py` → kelas `ConditionBuilder`),
  ditambah `base_builder.py` sebagai basis.
- `src/terminology/terminology_client.py` → `TerminologyClient` (PAT statis menang; bila kosong dan
  kredensial OIDC ada, token diambil malas lalu disimpan sampai kedaluwarsa).
- Versi dinaikkan bersama tiga SDK lain (lihat `docs/PRD-SDK-ECOSYSTEM.md` §3).

## 5. Selisih Nyata terhadap SDK PHP (diukur)

| Kemampuan | PHP | Python | Bukti |
|---|---|---|---|
| Bangun payload FHIR | 141 `PayloadBuilder*` | **140 kelas** | `grep -c "^class .*Builder"` |
| Nilai bertipe (DataType) | 32 | **33** | `src/datatype` |
| Kirim FHIR + retry/refresh | `SSRequest` | **TIDAK ADA** | `find src -iname "*ssrequest*"` → kosong |
| Bungkus jawaban + 558 aturan validasi | `SSResponse`, `SSValidationError` | **TIDAK ADA** | idem |
| Parser FHIR | 18 berkas | **TIDAK ADA** | `find src -iname "*parser*"` → kosong |
| Antrean kirim | 8 berkas | 3 penyusun | `ls src/queue` |
| Klien terminology | 22 berkas | 27 berkas | `ls src/terminology` |

**Kesimpulan:** sama seperti SDK Node — ini **pembangun payload + klien terminology**, bukan SDK
pengiriman. Selisih ini harus dinyatakan, bukan disembunyikan.

## 6. Pemetaan Galat (`TerminologyClient`)

- `timeout` bawaan **30 detik** (`timeout: int = 30`).
- `requests.RequestException` → `RuntimeError("TerminologyClient network error: …")` — jaringan
  dibedakan dari HTTP, berbeda dari SDK Node.
- **401** → bila PAT kosong dan kredensial OIDC ada, satu percobaan ulang dengan token baru.
- **>= 400** → `RuntimeError("TerminologyClient HTTP <status>: …")`; badan jawaban ikut bila ada.
- Badan jawaban non-JSON ditangani `except ValueError` → tidak melempar galat urai.

## 7. Uji

```bash
uv run --with pytest --with requests --with pydantic pytest src -q
```

**Hasil terukur 2026-10-27:** `79 passed in 0.89s` — pertama kali suite ini benar-benar dijalankan
di mesin ini (sebelumnya pytest tidak terpasang di venv, sehingga statusnya "belum diukur").
Berkas uji: `test_builders.py`, `test_report.py`, `test_script.py`, `test_datatypes.py`,
`test_terminology_client.py`. Jumlah fungsi `def test_` = 54; pytest melaporkan 79 karena sebagian
fungsi diparametrisasi.

## 8. Utang Teknis & Langkah Berikut

- **T-01** ~~`pyproject.toml` menyebut "115 PayloadBuilder classes", nyata 140.~~ **SELESAI
  2026-10-27**: `pyproject.toml` (description) dan `README.md` (2 tempat) kini menyebut **140**.
  Angka itu memakai metrik yang sama dengan manifest paritas, dan dapat diukur ulang dengan:
  `grep -rhoE '^class [A-Za-z0-9_]+Builder' src/builder --include='*.py' --exclude='test_*.py' | wc -l`
- **T-02** `SYNC_MANIFEST.json` menyatakan semua komponen `pending` dengan total 51 builder; nyata 140.
  Diperbaiki pada commit yang sama dengan dokumen ini.
- **T-03** Tidak ada lapisan pengiriman FHIR (`SSRequest`/`SSResponse`) maupun Parser. Keputusan pemilik
  produk: port dari PHP atau nyatakan SDK ini "payload builder only" di README + PRD.
- **T-04** `__test__ = False` sudah dipakai pada kelas domain berawalan `Test` (TestReport/TestScript)
  supaya pytest tidak salah kumpulkan — pertahankan saat menambah resource baru.
- **Berikutnya:** SRD untuk `-go`, lalu perbaiki manifest ketiga repo.
