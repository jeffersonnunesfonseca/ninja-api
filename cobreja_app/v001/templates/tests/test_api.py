import pytest
from django.test import Client

from cobreja_app.shareds.enum import EnvrionmentEnum


@pytest.mark.django_db
def test_health_endpoint():
    client = Client()
    response = client.get(
        "/cobreja/v001/templates/_health",
        headers={"X-TOKEN": EnvrionmentEnum.DEVELOPMENT},
    )

    assert "TEMPLATES_OK_" in response.text
    assert response.status_code == 200
