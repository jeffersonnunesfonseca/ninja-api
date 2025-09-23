from time import time

from .router import router


@router.get("/_health")
async def health(request):
    return f"INSTALLMENTS_OK_{time()}"
