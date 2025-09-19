# core/middleware.py
from django.http import JsonResponse


class CustomResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # só intercepta JSON
        if isinstance(response, JsonResponse):
            data = response.json()
            custom = {
                "success": True,
                "data": data,
                "errors": None,
            }
            return JsonResponse(custom, status=response.status_code)

        return response
