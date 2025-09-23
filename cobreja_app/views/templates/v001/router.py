from ninja import Router

from core.security.auth import AuthToken

router = Router(tags=["TemplatesV001"], auth=AuthToken())
