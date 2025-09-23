import pytest
from django.test import Client

from cobreja_app.shareds.enum import EnvrionmentEnum


@pytest.mark.django_db
def test_rule_steps_health_endpoint():
    client = Client()
    response = client.get(
        "/cobreja/api/rule_steps/v001/_health",
        headers={"X-TOKEN": EnvrionmentEnum.DEVELOPMENT},
    )

    assert "RULE_STEPS_OK_" in response.text
    assert response.status_code == 200
