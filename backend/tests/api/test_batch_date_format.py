def test_batch_accepts_and_returns_br_date(client, auth_setup):
    payload = {
        "name": "Lote Novilhas",
        "batch_purpose": "Reproducao",
        "status": "ACTIVE",
        "category": "HEIFER",
        "check_in": "28/05/2026",
        "check_out": None,
        "property_id": auth_setup["property"].id_property,
    }
    create_resp = client.post(
        "/batches/",
        json=payload,
        headers=auth_setup["headers"],
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["check_in"] == "28/05/2026"



