from time import time

from ninja import Router

router = Router(tags=["Charges"])


@router.get("/_health")
def health(request):
    return f"CHARGES_OK_{time()}"


# @router.get("/_health")
# async def health(request, delay: int, word: str):
#     print("Thread:", current_thread().name)
#     await asyncio.sleep(delay)
#     return f"CHARGES_OK_{time()}"


# @router.get("/_health_blocking")
# def health_blocking(request, delay: int, word: str):
#     print("Thread:", current_thread().name)
#     sleep(delay)
#     return f"BLOCKING_CHARGES_OK_{time()}"
