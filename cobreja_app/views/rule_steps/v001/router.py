from ninja import Router

from core.security.auth import AuthToken

router = Router(tags=["RuleStepsV001"], auth=AuthToken())
