from litestar import Router
from routes.germplasm.controllers.germplasm import GermplasmController

GermplasmRouter = Router(
    path='/brapi/v2',
    tags=['Germplasm'],
    route_handlers=[
        GermplasmController
    ]
)
