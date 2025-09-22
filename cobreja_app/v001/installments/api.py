from time import time

from ninja import Router

router = Router(tags=["Installments"])


@router.get("/_health")
async def health(request):
    return f"INSTALLMENTS_OK_{time()}"
