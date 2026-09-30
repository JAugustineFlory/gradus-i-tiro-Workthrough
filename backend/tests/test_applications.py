SAMPLE = {
    "company": "Acme",
    "role": "Junior Developer",
    "applied_on": "2026-10-01",
}

def create_sample(client, **overrides):
    payload = {**SAMPLE, **overrides}
    response = client.post("/applications", json=payload)
    return response.json()


def test_create_application_returns_201_and_the_row(client):
    response = client.post("/applications", json=SAMPLE)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["company"] == "Acme"
    assert body["status"] == "applied"
    assert body["applied_on"] == "2026-10-01"

def test_create_without_company_returns_422(client):
    payload = {
        "role": "Junior Developer",
        "applied_on": "2026-10-01",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 422

def test_list_applications_starts_empty(client):
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == []


def test_list_returns_every_application_in_order(client):
    create_sample(client, company="Acme")
    create_sample(client, company="Globex")

    response = client.get("/applications")

    companies = [item["company"] for item in response.json()]
    assert companies == ["Acme", "Globex"]