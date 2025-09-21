from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from core.db_router import get_current_tenant
from core.exceptions import (
    NotAllowedInNonDevelopmentEnvironmentError,
    TenantNotFoundError,
)
from core.middleware import MultiTenantMiddleware


@pytest.fixture
def fake_redis():
    """Cria um fake Redis e aplica patch apenas quando usado"""
    fake = MagicMock()
    with patch(
        "core.middleware.get_redis_connection"
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
    # @override_settings(ENVIRONMENT="development") só funciona se tiver usando o
    # settings do django e nao do pydantic
    def test_without_token_env_dev(self, rf):
        request = rf.get("/")  # sem header X-TOKEN
        mw = MultiTenantMiddleware(lambda r: r)

        response = mw.process_request(request)

        assert "tenant_db_alias" not in request
        assert get_current_tenant() == "default"
        assert response is None  # não bloqueia

    def test_with_token_env_dev_without_tenant_created(self, rf):
        request = rf.get("/", HTTP_X_TOKEN="tenant123")
        mw = MultiTenantMiddleware(lambda r: r)
        with pytest.raises(TenantNotFoundError):
            mw.process_request(request)

    def test_with_token_env_dev(self, rf, fake_redis):
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

    def test_without_token_env_prod(self, rf):
        request = rf.get("/")

        mw = MultiTenantMiddleware(lambda r: r)

        with (
            patch("core.config.settings.ENVIRONMENT", "production"),
            pytest.raises(NotAllowedInNonDevelopmentEnvironmentError),
        ):
            mw.process_request(request)
