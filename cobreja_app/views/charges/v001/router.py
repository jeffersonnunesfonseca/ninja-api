from ninja import Router

from core.security.auth import AuthToken

router = Router(tags=["ChargesV001"], auth=AuthToken())
