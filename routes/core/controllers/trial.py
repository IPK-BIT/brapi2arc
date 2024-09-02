from litestar import Controller, get
from litestar.datastructures import State
from arctrl.arctrl import JsonController
import json

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.core import Trial


class TrialController(Controller):
    path = '/trials'

    @get('/')
    async def get_trials(self, state: State, programDbId: str | None = None) -> Response[Trial]:
        isa = json.loads(JsonController.Investigation().to_isajson_string(
            JsonController.ARC().from_rocrate_json_string(state.rocrate).ISA
        ))

        trials = [
            Trial(
                trialDbId=isa['identifier'],
                trialName=isa['title'],
                trialDescription=isa['description'],
            )
        ]

        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=1,
                    totalPages=1
                ),
                datafiles=[],
                status=[
                    Message(
                        messageType=MESSAGETYPE.INFO,
                        message='Success'
                    )
                ]
            ),
            result=Result(
                data=trials
            )
        )
