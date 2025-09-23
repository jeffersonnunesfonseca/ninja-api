from ninja import Router

from core.security.auth import AuthToken

router = Router(tags=["InstallmentsV001"], auth=AuthToken())
