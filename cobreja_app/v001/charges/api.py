from time import time

from ninja import Router

router = Router(tags=["Charges"])


@router.get("/_health")
def health(request):
    return f"CHARGES_OK_{time()}"
