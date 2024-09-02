from litestar import Router
from routes.search.controllers.observation_variable import ObservationVariableSearchController
from routes.search.controllers.germplasm import GermplasmSearchController

SearchRouter = Router(
    path='/brapi/v2/search',
    route_handlers=[
        GermplasmSearchController,
        ObservationVariableSearchController
    ]
)
