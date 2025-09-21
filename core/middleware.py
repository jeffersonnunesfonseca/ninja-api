from http import HTTPStatus

from django.db import connections
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

from cobreja_app.shareds.enum import EnvrionmentEnum
from core.config import settings
from core.db_router import set_current_tenant


class MultiTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Pega os headers do tenant
        token = request.headers.get("X-TOKEN")
        if not token:
            return HttpResponse("X-TOKEN required", status=HTTPStatus.UNAUTHORIZED)

        if token == EnvrionmentEnum.DEVELOPMENT:
            return self._to_dev()

        redis_client = get_redis_connection("default")

        tenant_data = redis_client.hgetall(f"tenant:{token}")
        if not tenant_data:
            return HttpResponse("X-TOKEN not configured", status=HTTPStatus.FORBIDDEN)

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

        # Define alias da request
        request.tenant_db_alias = "tenant"
        # Define globalmente para o router via thread local
        set_current_tenant("tenant")
        return None

    def _to_dev(self):
        """Não deixa ser single tenant em produção"""
        if settings.ENVIRONMENT != EnvrionmentEnum.DEVELOPMENT:
            return HttpResponse(
                "Only development use single tenant",
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        set_current_tenant("default")
        return None
