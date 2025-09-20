import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_endpoint():
    client = Client()
    response = client.get("/cobreja/v001/rules/_health")

    assert "RULES_OK_" in response.text
    assert response.status_code == 200
