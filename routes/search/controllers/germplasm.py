from dataclasses import dataclass
from litestar import Controller, post
from litestar.datastructures import State
from arctrl.arctrl import JsonController
import json

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.germplasm import Germplasm


class GermplasmSearchController(Controller):
    path = '/germplasm'
    tags = ['Germplasm']

    @dataclass
    class GermplasmSearch:
        germplasmName: list[str]

    @post('/')
    async def search_germplasm(self, state: State, data: GermplasmSearch) -> Response[Germplasm]:
        isa = json.loads(JsonController.Investigation().to_isajson_string(
            JsonController.ARC().from_rocrate_json_string(state.rocrate).ISA
        ))

        filtered_inputs = []
        for study in isa['studies']:
            for process in study['processSequence']:
                if process['executesProtocol']['name'] == 'Growth':
                    for input in process['inputs']:
                        if input['name'] in data.germplasmName:
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
