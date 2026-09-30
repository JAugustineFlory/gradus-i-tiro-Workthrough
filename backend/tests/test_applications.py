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


def test_get_application_by_id(client):
    created = create_sample(client)

    response = client.get(f"/applications/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_application_returns_404(client):
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_update_changes_only_the_fields_sent(client):
    created = create_sample(client)

    response = client.patch(
        f"/applications/{created['id']}",
        json={"status": "interviewing"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "interviewing"
    assert body["company"] == "Acme"


def test_update_missing_application_returns_404(client):
    response = client.patch(
        "/applications/999",
        json={"status": "offer"},
    )

    assert response.status_code == 404