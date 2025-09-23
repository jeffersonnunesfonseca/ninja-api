from time import time

from .router import router


@router.get("/_health")
def health(request):
    return f"RULES_OK_{time()}"
