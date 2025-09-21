from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from cobreja_app.shareds.enum import EnvrionmentEnum
from core.db_router import get_current_tenant
from core.middlewares.multi_tenant_middleware import MultiTenantMiddleware


@pytest.fixture
def fake_redis():
    """Cria um fake Redis e aplica patch apenas quando usado"""
    fake = MagicMock()
    with patch(
        "core.middlewares.multi_tenant_middleware.get_redis_connection"
    ) as mock_redis:  # substitui o Redis real pelo mock
        mock_redis.return_value = fake
        yield fake

    # Limpa qualquer configuração após o teste
    fake.reset_mock()


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.django_db
class TestMultiTenantMiddleware:
    def test_without_token(self, rf):
        request = rf.get("/")  # sem header X-TOKEN
        mw = MultiTenantMiddleware(lambda r: r)

        response = mw.process_request(request)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_without_tenant_created(self, rf):
        request = rf.get("/", HTTP_X_TOKEN="tenant123")
        mw = MultiTenantMiddleware(lambda r: r)
        response = mw.process_request(request)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_token(self, rf, fake_redis):
        fake_redis.hgetall.return_value = {
            b"db_name": b"testdb",
            b"db_user": b"user",
            b"db_password": b"pass",
            b"db_host": b"localhost",
            b"db_port": b"5432",
            b"db_engine": b"django.db.backends.sqlite3",
        }

        request = rf.get("/", HTTP_X_TOKEN="tenant123")
        mw = MultiTenantMiddleware(lambda r: r)

        mw.process_request(request)
        assert request.tenant_db_alias == "tenant"
        assert get_current_tenant() == "tenant"

    def test_with_dev_token_env_prod(self, rf):
        request = rf.get("/", HTTP_X_TOKEN=EnvrionmentEnum.DEVELOPMENT)

        mw = MultiTenantMiddleware(lambda r: r)

        with patch("core.config.settings.ENVIRONMENT", EnvrionmentEnum.PRODUCTION):
            response = mw.process_request(request)
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
            assert response.content == b"Only development use single tenant"
