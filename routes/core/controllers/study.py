from litestar import Controller, get
from litestar.datastructures import State
from arctrl.arctrl import JsonController
import json

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.core import Study


class StudyController(Controller):
    path = '/studies'

    @get('/')
    async def get_studies(self, state: State, trialDbId: str | None = None) -> Response[Study]:
        # TODO: if implementing multiple program support, trialDbId should be used to retrieve the correct ARC.
        # FIXME: how does the studyType play into this?

        isa = json.loads(JsonController.Investigation().to_isajson_string(
            JsonController.ARC().from_rocrate_json_string(state.rocrate).ISA
        ))

        studies = []
        for study in isa['studies']:
            studies.append(
                Study(
                    studyDbId=study['identifier'],
                    studyName=study['title'],
                )
            )

        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=len(studies),
                    totalPages=len(studies) // 1000 +
                    (1 if len(studies) % 1000 > 0 else 0)
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
                data=studies
            )
        )
