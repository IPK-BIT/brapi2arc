from litestar import Controller, get

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result


class StudyTypesController(Controller):
    path = '/studytypes'

    @get('/')
    async def get_study_types(self) -> Response[str]:
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
                data=['Field Study']
            )
        )
