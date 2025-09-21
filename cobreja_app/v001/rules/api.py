from time import time

from ninja import Router

router = Router(tags=["Rules"])


@router.get("/_health")
def health(request):
    return f"RULES_OK_{time()}"
