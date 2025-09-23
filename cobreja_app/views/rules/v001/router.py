from ninja import Router

from core.security.auth import AuthToken

router = Router(tags=["RulesV001"], auth=AuthToken())
