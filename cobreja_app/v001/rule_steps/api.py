from time import time

from ninja import Router

router = Router(tags=["RuleSteps"])


@router.get("/_health")
async def health(request):
    return f"RULE_STEPS_OK_{time()}"
