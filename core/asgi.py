"""
ASGI config for core project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

# Define o settings module do Django antes de qualquer importação que dependa dele
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.asgi import get_asgi_application

# Import OpenTelemetry setup depois que os settings estão definidos
import core.otel_setup  # noqa: F401

application = get_asgi_application()
