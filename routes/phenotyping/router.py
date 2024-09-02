from litestar import Router
from routes.phenotyping.controllers.observation import ObservationController
from routes.phenotyping.controllers.observation_unit import ObservationUnitController
from routes.phenotyping.controllers.observation_variable import ObservationVariableController

PhenotypingRouter = Router(
    path='/brapi/v2',
    tags=['Phenotyping'],
    route_handlers=[
        ObservationController,
        ObservationUnitController,
        ObservationVariableController
    ]
)
