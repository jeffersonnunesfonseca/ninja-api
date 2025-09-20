import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_endpoint():
    client = Client()
    response = client.get("/cobreja/v001/installments/_health")

    assert "INSTALLMENTS_OK_" in response.text
    assert response.status_code == 200
