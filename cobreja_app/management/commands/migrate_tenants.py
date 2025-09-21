# cobreja_app/management/commands/migrate_tenants.py
import json

from django.core.cache import cache  # django-redis
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Roda migrate para todos os tenants cadastrados no Redis"

    def handle(self, *args, **kwargs):
        # Supondo que todos os tenants estão no Redis com key "tenant:<token>"
        # Exemplo: tenant_data = {"db_engine": ..., "db_name": ..., etc.}

        # Para simplificar, pega todas as keys
        keys = cache.keys("tenant:*")
        if not keys:
            self.stdout.write(self.style.WARNING("Nenhum tenant encontrado no Redis"))
            return

        for key in keys:
            tenant_data_json = cache.get(key)
            if not tenant_data_json:
                continue

            tenant_data = json.loads(tenant_data_json)
            alias = key.split(":")[1]  # exemplo: tenant:abc123 -> abc123

            # registra a conexão temporariamente
            connections.databases[alias] = {
                "ENGINE": tenant_data["db_engine"],
                "NAME": tenant_data["db_name"],
                "USER": tenant_data.get("db_user", ""),
                "PASSWORD": tenant_data.get("db_password", ""),
                "HOST": tenant_data.get("db_host", "localhost"),
                "PORT": str(tenant_data.get("db_port", 5432)),
            }

            self.stdout.write(f"Rodando migrate para {alias}...")
            call_command("migrate", database=alias)
            self.stdout.write(self.style.SUCCESS(f"Migrations aplicadas para {alias}"))
