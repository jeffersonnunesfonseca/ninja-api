from time import time

from ninja import Router

router = Router(tags=["Templates"])


@router.get("/_health")
def health(request):
    return f"TEMPLATES_OK_{time()}"
