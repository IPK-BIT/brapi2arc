from litestar import Controller, get
from litestar.datastructures import State
from arctrl.arctrl import JsonController
import json


from models.response import Response, Message, Metadata, Pagination, Result, MESSAGETYPE
from models.germplasm import Germplasm


class GermplasmController(Controller):
    path = '/germplasm'

    @get('/')
    async def get_germplasm(self, state: State, germplasmName: str | None = None) -> Response[Germplasm]:
        isa = json.loads(JsonController.Investigation().to_isajson_string(
            JsonController.ARC().from_rocrate_json_string(state.rocrate).ISA
        ))

        filtered_inputs = []
        for study in isa['studies']:
            for process in study['processSequence']:
                if process['executesProtocol']['name'] == 'Growth':
                    for input in process['inputs']:
                        if germplasmName is None or input['name'] in germplasmName.split(','):
                            germplasm = Germplasm(
                                germplasmDbId=input['name'],
                                germplasmName=input['name'],
                            )
                            if germplasm not in filtered_inputs:
                                filtered_inputs.append(germplasm)

        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=len(filtered_inputs),
                    totalPages=len(filtered_inputs) // 1000 +
                    (1 if len(filtered_inputs) % 1000 > 0 else 0)
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
                data=filtered_inputs
            )
        )
