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
import pandas as pd

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
                                        entryType=next(
                                            (prop['value'] for prop in output['additionalProperties'] if prop['category'] == 'ENTRY TYPE'), None),
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
    
    #TODO: Only commit if there are changes
    @post('/')
    async def post_observation_units(self, state: State, headers: dict, data: list[ObservationUnit]) -> Response[ObservationUnit]:
        token = headers.get('authorization').split(' ')[1]
        written_observation_units = []

        df = pd.DataFrame([ob.__dict__ for ob in data])

        actions = []

        arc_obj = arc.read('data/')
        study_grouped_df = df.groupby('studyDbId')
        for studyDbId, study_group in study_grouped_df:
            changes = False
            study = arc_obj.ISA.GetStudy(studyDbId)
            germplasm_grouped_df = study_group.groupby('germplasmDbId')
            germplasm_index = {}
            growth = study.GetTable('Growth')
            for i in range(0, growth.RowCount):
                row = study.GetTable('Growth').GetRow(i)
                germplasm_index[row[0].AsFreeText] = i

            growth_header = growth.Headers
            new_growth = ArcTable.init('Growth')
            for header in growth_header:
                new_growth.AddColumn(header)
            
            column_index = {}
            for i in range(0, len(growth_header)):
                column_index[str(growth_header[i])] = i
            for germplasmDbId, germplasm_group in germplasm_grouped_df:
                for _, germplasm_row in germplasm_group.iterrows():
                    row = growth.GetRow(germplasm_index[germplasmDbId])
                    if row[-1].AsFreeText != '':
                        continue
                    new_growth.AddRow(row)
                    pos: Position = germplasm_row['observationUnitPosition']
                    i = new_growth.RowCount - 1
                    if pos.positionCoordinateX and pos.positionCoordinateY:
                        observationUnitDbId = f'{germplasmDbId}-{pos.positionCoordinateX}-{pos.positionCoordinateY}'
                    else:
                        observationUnitDbId = f'{germplasmDbId}-{uuid1()}'
                    new_growth.UpdateCellAt(column_index['Output [Sample Name]'], i, CompositeCell.free_text(observationUnitDbId))
                    if pos.entryType:
                        new_growth.UpdateCellAt(column_index['Factor [ENTRY TYPE]'], i, CompositeCell.term(OntologyAnnotation(pos.entryType,'',''))) 
                    if pos.positionCoordinateX:
                        new_growth.UpdateCellAt(column_index['Factor [GRID COLUMN]'], i, CompositeCell.term(OntologyAnnotation(pos.positionCoordinateX,'','')))
                    if pos.positionCoordinateY:
                        new_growth.UpdateCellAt(column_index['Factor [GRID ROW]'], i, CompositeCell.term(OntologyAnnotation(pos.positionCoordinateY,'','')))
                    if pos.observationLevel:
                        new_growth.UpdateCellAt(column_index['Factor [REPLICATE]'], i, CompositeCell.term(OntologyAnnotation(pos.observationLevel.levelCode,'','')))
                    ou=ObservationUnit(**germplasm_row.to_dict())
                    ou.observations = None
                    ou.observationUnitDbId = observationUnitDbId
                    ou.observationUnitName = observationUnitDbId
                    written_observation_units.append(ou)
                    changes = True
            if changes:
                included_germplasms = set(new_growth.GetColumn(0).Cells[i].AsFreeText for i in range(new_growth.RowCount))
                for key, i in germplasm_index.items():
                    if key not in included_germplasms:
                        new_growth.AddRow(growth.GetRow(i))

                study.UpdateTable('Growth', new_growth)
                spreadsheet = XlsxController().Study().to_fs_workbook(study)
                Xlsx().to_xlsx_file(
                    f'data/studies/{studyDbId}/isa.study.xlsx', spreadsheet)
            
                actions.append(
                    {
                        'action': 'update',
                        'file_path': f'studies/{studyDbId}/isa.study.xlsx',
                        'encoding': 'base64',
                        'content': base64.b64encode(open(f'data/studies/{studyDbId}/isa.study.xlsx', 'rb').read()).decode('utf-8')
                    }
                )
        if len(actions)>0:
            arc_obj = arc.read('data/')
            arc_rocrate = JsonController().ARC().to_rocrate_json_string()(arc_obj)
        
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
