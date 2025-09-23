import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# Import OpenTelemetry setup before Django initialization
from django.core.wsgi import get_wsgi_application

# Deve manter nessa ordem
import core.telemetry.otel_setup  # noqa: F401

application = get_wsgi_application()
