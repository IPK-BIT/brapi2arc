from icecream import ic

from litestar import Controller, get, post
from litestar.datastructures import State
from arctrl.arctrl import ArcTable, CompositeHeader, CompositeCell, IOType, XlsxController, OntologyAnnotation
from fsspreadsheet.xlsx import Xlsx
from utils import arc
from arctrl.arctrl import JsonController
from uuid import uuid1
import git
import datetime
import json
import base64
import requests
import os

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
    async def post_observation_units(self, state: State, headers: dict, data: list[ObservationUnit]) -> Response[ObservationUnit]:
        token = headers.get('authorization').split(' ')[1]
        written_observation_units = []

        arc_obj = arc.read('data/')
        actions = []

        index_mapping = {}

        for study in arc_obj.ISA.Studies:
            growth = study.GetTable('Growth')
            index_mapping[study.Identifier] = {}
            for i in range(0,growth.RowCount):
                index_mapping[study.Identifier][growth.GetRow(i)[0].AsFreeText] = i

        for observation_unit in data:
            study = arc_obj.ISA.GetStudy(observation_unit.studyDbId)
            growth = study.GetTable('Growth')
            #TODO: Mapping to query the observation unit from the growth table
            
            i=index_mapping[observation_unit.studyDbId][observation_unit.germplasmDbId]
            row = growth.GetRow(i)
            if row[-1].AsFreeText == '':
                if row[0].AsFreeText == observation_unit.germplasmDbId:
                    if observation_unit.observationUnitPosition.positionCoordinateX and observation_unit.observationUnitPosition.positionCoordinateY:
                        observation_unit.observationUnitDbId = f'{observation_unit.germplasmDbId}-{observation_unit.observationUnitPosition.positionCoordinateX}-{observation_unit.observationUnitPosition.positionCoordinateY}'
                    else:
                        observation_unit.observationUnitDbId = f'{observation_unit.germplasmDbId}-{uuid1()}'
                    growth.UpdateCellAt(8,i,CompositeCell.free_text(observation_unit.observationUnitDbId))
                    if observation_unit.observationUnitPosition:
                        if observation_unit.observationUnitPosition.positionCoordinateX:
                            growth.UpdateCellAt(7, i, CompositeCell.term(OntologyAnnotation(observation_unit.observationUnitPosition.positionCoordinateX,'','')))
                        if observation_unit.observationUnitPosition.positionCoordinateY:
                            growth.UpdateCellAt(6, i, CompositeCell.term(OntologyAnnotation(observation_unit.observationUnitPosition.positionCoordinateY,'','')))
                        if observation_unit.observationUnitPosition.observationLevel:
                            growth.UpdateCellAt(5, i, CompositeCell.term(OntologyAnnotation(observation_unit.observationUnitPosition.observationLevel.levelCode,'','')))
                    study.UpdateTable('Growth', growth)
            spreadsheet = XlsxController().Study().to_fs_workbook(study)
            Xlsx().to_xlsx_file(
                f'data/studies/{observation_unit.studyDbId}/isa.study.xlsx', spreadsheet)
            observation_unit.observations = None
            written_observation_units.append(observation_unit)
        arc_obj = arc.read('data/')
        arc_rocrate = JsonController().ARC().to_rocrate_json_string()(arc_obj)
        actions.append(
                {
                    'action': 'update',
                    'file_path': f'studies/{observation_unit.studyDbId}/isa.study.xlsx',
                    'encoding': 'base64',
                    'content': base64.b64encode(open(f'data/studies/{observation_unit.studyDbId}/isa.study.xlsx', 'rb').read()).decode('utf-8')
                }
            )
        actions.append({
            'action': 'update',
            'file_path': 'metadata.json',
            'encoding': 'text',
            'content': arc_rocrate
        })
        json_payload = {
            'branch': 'main',
            'commit_message': f'[brapi2arc] Add observation units - {datetime.datetime.now()}',
            'actions': actions
        }
        response = requests.post(f'{os.getenv("DATAHUB_URL")}api/v4/projects/{os.getenv("ARC_URI").replace("/","%2F")}/repository/commits', headers={
            'PRIVATE-TOKEN': token
        }, json=json_payload)
        response.raise_for_status()
        
        for root, dirs, files in os.walk('data', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        git.Repo.clone_from(f"{os.getenv('DATAHUB_URL')}{os.getenv('ARC_URI')}", 'data')
        metadata_path = 'data/metadata.json'
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as file:
                state.rocrate = file.read()

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
                data=written_observation_units
            )
        )
