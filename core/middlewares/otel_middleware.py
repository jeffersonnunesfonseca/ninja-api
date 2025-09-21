from django.utils.deprecation import MiddlewareMixin
from opentelemetry import trace


class OTELCustomHeadersMiddleware(MiddlewareMixin):
    """
    Middleware Django para adicionar atributos customizados aos spans do OpenTelemetry.
    - Captura o header X-TOKEN
    - Captura status code da resposta
    - (Opcional) captura body da resposta
    """

    def process_request(self, request):
        span = trace.get_current_span()
        if span.is_recording():
            token = request.headers.get("X-TOKEN")
            if token:
                span.set_attribute("http.request.header.x-token", token)
        # Retorna None para continuar o fluxo normal
        return

    def process_response(self, request, response):
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("http.response.status_code", response.status_code)

            # Opcional: adicionar body (atenção, pode ser grande!)
            try:
                body = response.content
                if isinstance(body, bytes):
                    body = body.decode(errors="ignore")
                span.set_attribute("http.response.body", body)
            except Exception:  # noqa: BLE001
                pass

        return response
