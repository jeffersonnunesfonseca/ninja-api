from ninja import NinjaAPI

from cobreja_app.views.charges.v001.router import router as charges_router_v001
from cobreja_app.views.installments.v001.router import (
    router as installments_router_v001,
)
from cobreja_app.views.rule_steps.v001.router import router as rule_steps_router_v001
from cobreja_app.views.rules.v001.router import router as rules_router_v001
from cobreja_app.views.templates.v001.router import router as templates_router_v001
from core.config import settings

api = NinjaAPI(version=settings.APP_VERSION, title="Cobreja API")

api.add_router("/cobreja/api/charges/v001/", charges_router_v001)
api.add_router("/cobreja/api/templates/v001/", templates_router_v001)
api.add_router("/cobreja/api/rules/v001/", rules_router_v001)
api.add_router("/cobreja/api/rule_steps/v001/", rule_steps_router_v001)
api.add_router("/cobreja/api/installments/v001/", installments_router_v001)
