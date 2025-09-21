import time

import psutil
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def get_system_metrics(options: CallbackOptions):
    """Callback function to collect system metrics"""
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=None)
    yield Observation(cpu_usage, {"resource": "cpu", "unit": "percent"})

    # Memory usage
    memory = psutil.virtual_memory()
    yield Observation(memory.percent, {"resource": "memory", "unit": "percent"})
    yield Observation(
        memory.used, {"resource": "memory", "unit": "bytes", "type": "used"}
    )
    yield Observation(
        memory.available, {"resource": "memory", "unit": "bytes", "type": "available"}
    )

    # Disk usage
    disk = psutil.disk_usage("/")
    disk_usage_percent = (disk.used / disk.total) * 100
    yield Observation(
        disk_usage_percent, {"resource": "disk", "unit": "percent", "mount": "/"}
    )


def get_application_metrics(options: CallbackOptions):
    """Callback function to collect application-specific metrics"""
    # Current timestamp
    yield Observation(time.time(), {"metric": "last_update", "unit": "timestamp"})

    # Active threads
    import threading

    active_threads = threading.active_count()
    yield Observation(active_threads, {"metric": "active_threads", "unit": "count"})


# Create resource with service information
resource = Resource(
    attributes={SERVICE_NAME: "cobreja_app", "environment": "production"}
)

# Create OTLP exporters
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",  # Default OTLP gRPC endpoint
    insecure=True,  # Set to False in production with proper TLS
)

otlp_metric_exporter = OTLPMetricExporter(
    endpoint="http://localhost:4317",
    insecure=True,
)

# Configure metrics
metric_reader = PeriodicExportingMetricReader(
    exporter=otlp_metric_exporter,
    export_interval_millis=5000,  # Changed from 10000 to 5000 for 5-second intervals
)

# Create and configure providers
trace_provider = TracerProvider(resource=resource)
metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

# Set up trace processor
processor = BatchSpanProcessor(otlp_trace_exporter)
trace_provider.add_span_processor(processor)

# Set global providers
trace.set_tracer_provider(trace_provider)
metrics.set_meter_provider(metric_provider)


# utilizado para instrumentação manual
tracer = trace.get_tracer("cobreja_app.tracer")
meter = metrics.get_meter("cobreja_app.meter")


# Create observable gauge
system_metrics = meter.create_observable_gauge(
    name="system_resource_usage",
    description="System resource utilization",
    unit="1",
    callbacks=[get_system_metrics],
)


app_metrics = meter.create_observable_gauge(
    name="application_metrics",
    description="Application-specific metrics",
    unit="1",
    callbacks=[get_application_metrics],
)


# Automatic instrumentation
DjangoInstrumentor().instrument()
SQLite3Instrumentor().instrument()

# Se você estiver usando requests em seu código
RequestsInstrumentor().instrument()
