from icecream import ic

from litestar import Controller, get
from litestar.datastructures import State
import requests

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.core import Program


class ProgramController(Controller):
    path = '/programs'

    @get('/')
    async def get_programs(self, state: State) -> Response[Program]:
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
                data=[Program(
                    programDbId='1',
                    programName='Breeding Program'
                )]
            )
        )
