from icecream import ic

from litestar import Controller, get, post
from arctrl.arctrl import JsonController
import json
from utils import arc

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.phenotyping import ObservationUnit, Position, ObservationLevel


class ObservationUnitController(Controller):
    path = '/observationunits'

    @get('/')
    async def get_observation_units(self, studyDbId: str | None = None) -> Response[ObservationUnit]:
        arc_obj = arc.read('data/')

        observation_units = []
        if studyDbId:
            try:
                studies = [arc_obj.ISA.GetStudy(studyDbId)]
            except:
                return Response(
                    metadata=Metadata(
                        pagination=Pagination(
                            currentPage=0,
                            pageSize=1000,
                            totalCount=0,
                            totalPages=0
                        ),
                        datafiles=[],
                        status=[
                            Message(
                                messageType=MESSAGETYPE.ERROR,
                                message='Study not found'
                            )
                        ]
                    ),
                    result=Result(
                        data=[]
                    )
                )
        else: 
            studies = arc_obj.ISA.Studies
        for study in studies:
            for process in json.loads(JsonController.Study().to_rocrate_json_string(study))['processSequence']:
                if process['executesProtocol']['name'] == 'Growth':
                    for i in range(0, len(process['outputs'])):
                        output = process['outputs'][i]
                        if output['name']:
                            observation_units.append(
                                ObservationUnit(
                                    observationUnitDbId=output['name'],
                                    observationUnitName=output['name'],
                                    observationUnitPosition=Position(
                                        entryType=None,
                                        geoCoordinates=None,
                                        observationLevel=ObservationLevel(
                                            levelName='rep',
                                            levelCode=next(
                                            (prop['value'] for prop in output['additionalProperties'] if prop['category'] == 'REPLICATE'), None)
                                        ),
                                        observationLevelRelationships=None,
                                        positionCoordinateX=next(
                                            (prop['value'] for prop in output['additionalProperties'] if prop['category'] == 'GRID COLUMN'), None),
                                        positionCoordinateXType=next(
                                            ('GRID_COL' for prop in output['additionalProperties'] if prop['category'] == 'GRID COLUMN'), None),
                                        positionCoordinateY=next(
                                            (prop['value'] for prop in output['additionalProperties'] if prop['category'] == 'GRID ROW'), None),
                                        positionCoordinateYType=next(
                                            ('GRID_ROW' for prop in output['additionalProperties'] if prop['category'] == 'GRID ROW'), None),
                                    ),
                                    germplasmDbId=process['inputs'][i]['name'],
                                    germplasmName=process['inputs'][i]['name'],
                                    studyDbId=study.Identifier,
                                    studyName=study.Title,
                                    trialDbId=arc_obj.ISA.Identifier,
                                    trialName=arc_obj.ISA.Title,
                                )
                            )

        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=len(observation_units),
                    totalPages=len(observation_units) // 1000 +
                    (1 if len(observation_units) % 1000 > 0 else 0)
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
                data=observation_units
            )
        )
    
    @post('/')
    async def post_observation_units(self, data: list[ObservationUnit]) -> Response[ObservationUnit]:
        ic(data)
        data=[]
        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=len(data),
                    totalPages=len(data) // 1000 +
                    (1 if len(data) % 1000 > 0 else 0)
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
                data=data
            )
        )
