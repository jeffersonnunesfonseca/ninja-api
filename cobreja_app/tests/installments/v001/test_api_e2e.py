import pytest
from django.test import Client

from cobreja_app.shareds.enum import EnvrionmentEnum


@pytest.mark.django_db
def test_installment_health_endpoint():
    client = Client()
    response = client.get(
        "/cobreja/api/installments/v001/_health",
        headers={"X-TOKEN": EnvrionmentEnum.DEVELOPMENT},
    )

    assert "INSTALLMENTS_OK_" in response.text
    assert response.status_code == 200
