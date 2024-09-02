from litestar import Router
from routes.core.controllers.program import ProgramController
from routes.core.controllers.trial import TrialController
from routes.core.controllers.study import StudyController
from routes.core.controllers.studytype import StudyTypesController

CoreRouter = Router(
    path='/brapi/v2',
    tags=['Core'],
    route_handlers=[
        ProgramController,
        TrialController,
        StudyController,
        StudyTypesController
    ]
)
