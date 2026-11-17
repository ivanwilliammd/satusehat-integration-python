from satusehat_integration.terminology import satusehat_nonstandard as ns


def test_semua_url_domain_kemkes():
    for nama, url in ns.ALL:
        assert url.startswith("https://fhir.kemkes.go.id/"), f"{nama}: {url}"


def test_sebelas_objek():
    assert len(ns.ALL) == 11


def test_tidak_ada_url_ganda():
    assert len({u for _, u in ns.ALL}) == len(ns.ALL)


def test_identifier_selalu_official():
    assert ns.official_identifier(ns.NIK_SYSTEM, "3171234567890001") == {
        "use": "official",
        "system": ns.NIK_SYSTEM,
        "value": "3171234567890001",
    }


def test_administrative_code_irisan():
    ext = ns.administrative_code([("province", "31"), ("city", "3171")])
    assert ext["url"] == ns.EXT_ADMINISTRATIVE_CODE
    assert ext["extension"] == [
        {"url": "province", "valueCode": "31"},
        {"url": "city", "valueCode": "3171"},
    ]
