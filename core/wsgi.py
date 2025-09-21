import os

# Import OpenTelemetry setup before Django initialization
import core.otel_setup  # noqa: F401

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
