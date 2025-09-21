from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

from core.db_router import set_current_tenant


class MultiTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Pega os headers do tenant
        token = request.headers.get("X-TOKEN")
        if token:
            redis_client = get_redis_connection("default")
            tenant_data = redis_client.hgetall(f"tenant:{token}")

            if not tenant_data:
                request.tenant_db_alias = "default"
                set_current_tenant("default")
                return

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
        else:
            request.tenant_db_alias = "default"
            set_current_tenant("default")
