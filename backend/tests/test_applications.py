SAMPLE = {
    "company": "Acme",
    "role": "Junior Developer",
    "applied_on": "2026-10-01",
}


def test_create_application_returns_201_and_the_row(client):
    response = client.post("/applications", json=SAMPLE)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["company"] == "Acme"
    assert body["status"] == "applied"
    assert body["applied_on"] == "2026-10-01"