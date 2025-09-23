from time import time

from .router import router


@router.get("/_health")
async def health(request):
    return f"RULE_STEPS_OK_{time()}"
