from django.urls import path
from ninja import NinjaAPI

from cobreja_app.v001.charges.api import router as charges_router_v001
from cobreja_app.v001.installments.api import router as installments_router_v001
from cobreja_app.v001.rule_steps.api import router as rule_steps_router_v001
from cobreja_app.v001.rules.api import router as rules_router_v001
from cobreja_app.v001.templates.api import router as templates_router_v001

api = NinjaAPI()

api.add_router("api/v001/charges/", charges_router_v001)
api.add_router("api/v001/templates/", templates_router_v001)
api.add_router("api/v001/rules/", rules_router_v001)
api.add_router("api/v001/rule_steps/", rule_steps_router_v001)
api.add_router("api/v001/installments/", installments_router_v001)


urlpatterns = [
    path("cobreja/", api.urls),
]
