# SRD — satusehat-integration (SDK SATUSEHAT FHIR R4 · Python)

Status: v2.0 · 2026-11-09 · Pendamping: `docs/PRD-SDK-ECOSYSTEM.md` (repo PHP) + `README.md`
Versi paket terpasang: **4.15.4** (`pyproject.toml`).

Seluruh angka di dokumen ini **diukur** dari checkout ini, bukan dari ingatan.
Bila kode berubah, perbarui dokumen ini di commit yang sama.

## 1. Ruang Lingkup

Cara kerja internal SDK: lapisan, kontrak publik, paritas penuh terhadap SDK PHP, pemetaan galat,
aturan kompatibilitas, dan hasil uji. Cara memakai SATUSEHAT ada di `README.md`.

## 2. Prinsip Arsitektur

1. **Paritas Penuh dari Pembangunan hingga Pengiriman.**
   - `src/builder`, `src/datatype` membangun payload FHIR R4 secara murni (tanpa jaringan).
   - `src/ssrequest` (`OAuth2Client`, `SSRequest`) menangani autentikasi OAuth2 SATUSEHAT (`DEV`/`STG`/`PROD`), pengiriman HTTP, auto-refresh token saat `401`, serta backoff eksponensial & `Retry-After` saat `429`/`5xx`.
   - `src/ssresponse` (`SSResponse`, `BundleResponse`, `SSValidationError`) membungkus respons HTTP dan memetakan seluruh **558 aturan validasi** (`RuleNumber`) SATUSEHAT beserta 14 kategori respons.
   - `src/parser` menyediakan **18 parser resource FHIR** identik dengan SDK PHP.
   - `src/queue` menyediakan **8 modul antrean asinkron berbasis SQLite** (`SqliteQueue`, `Worker`, `QueueMonitor`, `RateLimiter`, `ErrorClassifier`, `QueueInterface`, `QueueResult`, `QueueException`).
   - `src/terminology` menyediakan `TerminologyClient` & `TerminologyResolver` untuk SmarTerm.
2. **Paket pip, bukan skrip.** Struktur `src/` dipasang lewat `pyproject.toml`; uji dijalankan dengan `python -m pytest src`.
3. **Rahasia hanya dari lingkungan atau argumen.** Kredensial SATUSEHAT maupun SmarTerm dibaca dari variabel lingkungan atau argumen konstruktor.
4. **Satu perilaku, empat bahasa.** Seluruh metode mendukung penamaan Pythonic `snake_case` sekaligus alias `camelCase` untuk kompatibilitas lintas SDK.

## 3. Inventaris Terukur

| Bagian | Jumlah | Detail |
|---|---|---|
| Berkas builder | 144 | `src/builder/*.py` (140 kelas `*Builder`) |
| Kelas DataType | 33 | `src/datatype/*.py` |
| Berkas `ssrequest` | 3 + 1 uji | `oauth2_client.py`, `ss_request.py`, `__init__.py`, `test_ssrequest.py` |
| Berkas `ssresponse` | 3 + 1 uji | `ss_response.py`, `bundle_response.py`, `ss_validation_error.py` (558 aturan), `test_ssresponse.py` |
| Berkas `parser` | 18 + `__init__.py` + 1 uji | 18 kelas `*Parser` di `src/parser/` |
| Berkas `queue` | 8 + `__init__.py` + 1 uji | `error_classifier.py`, `monitor.py`, `queue_exception.py`, `queue_interface.py`, `queue_result.py`, `rate_limiter.py`, `sqlite_queue.py`, `worker.py` |
| Berkas `terminology` | 27 | `src/terminology/*.py` |
| Berkas uji | 9 | `test_builders.py`, `test_report.py`, `test_script.py`, `test_datatypes.py`, `test_terminology_client.py`, `test_ssrequest.py`, `test_ssresponse.py`, `test_parsers.py`, `test_queue.py` |
| **Hasil pytest** | **92 lulus, 0 gagal** | `python -m pytest src -v` |

## 4. Kontrak Publik

- Nama paket PyPI: `satusehat-integration`; modul `src/` (lihat `[project]` di `pyproject.toml`).
- Ekspor tingkat atas (`src/__init__.py`):
  - `OAuth2Client`, `OAuth2ClientException`, `SSRequest`
  - `SSResponse`, `BundleResponse`, `SSValidationError`
  - Ke-18 kelas `*Parser` (`DeviceParser` .. `TaskParser`)
  - Ke-8 kelas `Queue` (`SqliteQueue`, `Worker`, `QueueMonitor`, `RateLimiter`, `ErrorClassifier`, `QueueInterface`, `QueueResult`, `QueueException`)
- Ekspor builder: satu modul per resource (`src/builder/condition.py` → kelas `ConditionBuilder`), ditambah `base_builder.py`.
- `src/terminology/terminology_client.py` → `TerminologyClient`.

## 5. Paritas terhadap SDK PHP (diukur)

| Kemampuan | PHP | Python | Status |
|---|---|---|---|
| Bangun payload FHIR | 141 `PayloadBuilder*` | **140 kelas** (+ `BaseBuilder`) | Paritas |
| Nilai bertipe (DataType) | 32 | **33** | Paritas |
| Kirim FHIR + retry/refresh | `OAuth2Client`, `SSRequest` | **`OAuth2Client`, `SSRequest`** | **100% Paritas** |
| Bungkus jawaban + 558 aturan validasi | `SSResponse`, `BundleResponse`, `SSValidationError` (558 aturan) | **`SSResponse`, `BundleResponse`, `SSValidationError` (558 aturan)** | **100% Paritas** |
| Parser FHIR | 18 berkas | **18 berkas** | **100% Paritas** |
| Antrean kirim (SQLite + Worker + Monitor) | 8 berkas | **8 berkas** | **100% Paritas** |
| Klien terminology | 22 berkas | **27 berkas** | **100% Paritas** |

## 6. Pemetaan Galat

- **`SSRequest`**:
  - **401** → jika `oauth2.is_token_auto_refresh()` aktif, panggil `refresh_token()` dan ulangi permintaan dengan backoff eksponensial (`2^n` detik, maks 60 detik) hingga `max_retries` (bawaan 5).
  - **429** → baca header `Retry-After` (atau `2^n` detik jika absen) dan ulangi hingga `max_retries`.
  - **5xx** → backoff eksponensial (`2^n` detik, maks 60 detik) hingga `max_retries`.
  - Kegagalan jaringan dikembalikan sebagai `SSResponse(0, OperationOutcome, message)` tanpa menjatuhkan proses pemanggil.
- **`TerminologyClient`**:
  - `timeout` bawaan **30 detik**.
  - `requests.RequestException` → `RuntimeError("TerminologyClient network error: …")`.
  - **401** → bila PAT kosong dan kredensial OIDC ada, satu percobaan ulang dengan token baru.
  - **>= 400** → `RuntimeError("TerminologyClient HTTP <status>: …")`.

## 7. Uji

```bash
python -m pytest src -v
```

**Hasil terukur:** `92 passed in 1.23s` (0 gagal).

## 8. Utang Teknis & Riwayat Penyelesaian

- **T-01** ~~`pyproject.toml` menyebut "115 PayloadBuilder classes", nyata 140.~~ **SELESAI**.
- **T-02** ~~`SYNC_MANIFEST.json` menyatakan semua komponen `pending`.~~ **SELESAI**.
- **T-03** ~~Tidak ada lapisan pengiriman FHIR (`SSRequest`/`SSResponse`), Parser, maupun Queue lengkap.~~ **SELESAI**: `OAuth2Client`, `SSRequest`, `SSResponse`, `BundleResponse`, `SSValidationError` (558 aturan), 18 kelas `Parser`, dan 8 berkas `Queue` (`SqliteQueue`, `Worker`, `QueueMonitor`, dll.) kini tersedia lengkap dengan pengujian unit.
- **T-04** `__test__ = False` dipertahankan pada kelas domain berawalan `Test` (`TestReport`/`TestScript`).
