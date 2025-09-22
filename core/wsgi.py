import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# Import OpenTelemetry setup before Django initialization
from django.core.wsgi import get_wsgi_application

import core.otel_setup  # noqa: F401

application = get_wsgi_application()
