from http import HTTPStatus

from django.db import connections
from django_redis import get_redis_connection
from ninja.errors import HttpError
from ninja.security import APIKeyHeader

from cobreja_app.shareds.enum import EnvrionmentEnum
from core.config import settings
from core.tenancy.db_router import set_current_tenant


class AuthToken(APIKeyHeader):
    param_name = "X-TOKEN"  # muda o header aceito

    def authenticate(self, request, token: str):
        if not token:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "X-TOKEN required")

        if token == EnvrionmentEnum.DEVELOPMENT:
            return self._to_dev()

        redis_client = get_redis_connection("default")
        tenant_data = redis_client.hgetall(f"tenant:{token}")

        if not tenant_data:
            raise HttpError(HTTPStatus.FORBIDDEN, "X-TOKEN not configured")

        connections.databases["tenant"] = {
            "ENGINE": tenant_data.get(
                b"db_engine", b"django.db.backends.postgresql"
            ).decode(),
            "NAME": tenant_data.get(b"db_name", b"").decode(),
            "USER": tenant_data.get(b"db_user", b"").decode(),
            "PASSWORD": tenant_data.get(b"db_password", b"").decode(),
            "HOST": tenant_data.get(b"db_host", b"").decode(),
            "PORT": tenant_data.get(b"db_port", b"5432").decode(),
        }

        request.tenant_db_alias = "tenant"
        set_current_tenant("tenant")
        return token

    def _to_dev(self):
        if settings.ENVIRONMENT != EnvrionmentEnum.DEVELOPMENT:
            raise HttpError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "Only development use single tenant",
            )
        set_current_tenant("default")
        return "default"
