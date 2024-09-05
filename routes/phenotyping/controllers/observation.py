from icecream import ic

from litestar import Controller, post
from litestar.datastructures import State
from arctrl.arctrl import ArcTable, CompositeHeader, CompositeCell, IOType, XlsxController, JsonController
from fsspreadsheet.xlsx import Xlsx
from utils import arc
import datetime
import base64
import requests
import os
import pandas as pd
import git

from models.response import Response, Message, Metadata, Pagination, MESSAGETYPE, Result
from models.phenotyping import Observation


class ObservationController(Controller):
    path = '/observations'

    @post('/')
    async def post_observations(self, state: State, headers: dict, data: list[Observation]) -> Response[Observation]:
        token = headers.get('authorization').split(' ')[1]

        arc_obj = arc.read('data')
        df = pd.DataFrame(
            columns=['Study', 'Assay Name', 'Date', 'Trait', 'Value'])
        for observation in data:
            df.loc[len(df)] = [observation.studyDbId, observation.observationUnitDbId,
                               observation.observationTimeStamp, observation.observationVariableDbId, observation.value]

        grouped_df = df.groupby('Study')
        written_observations = []
        actions = []
        for studyDbId, group in grouped_df:
            for assay in arc_obj.ISA.Assays:
                if assay.Identifier == studyDbId:
                    try:
                        phenotyping = assay.GetTable('Phenotyping')
                    except:
                        phenotyping = ArcTable.init('Phenotyping')
                        phenotyping.AddColumn(
                            CompositeHeader.input(IOType.sample()))
                        phenotyping.AddColumn(CompositeHeader.protocol_ref())
                        phenotyping.AddColumn(CompositeHeader.protocol_type())
                        phenotyping.AddColumn(
                            CompositeHeader.protocol_description())
                        phenotyping.AddColumn(CompositeHeader.protocol_uri())
                        phenotyping.AddColumn(
                            CompositeHeader.protocol_version())
                        phenotyping.AddColumn(
                            CompositeHeader.output(IOType.raw_data_file()))

                    # TODO: This is naive code.
                    observation_units = group['Assay Name'].unique()
                    already_added_units = [
                        str(cell) for cell in phenotyping.GetColumn(0).Cells]
                    observation_units = [
                        observation_unit for observation_unit in observation_units if observation_unit not in already_added_units]
                    for observation_unit in observation_units:
                        phenotyping.AddRow([
                            CompositeCell.free_text(observation_unit),
                            CompositeCell.free_text('Phenotyping'),
                            CompositeCell.empty_term(),
                            CompositeCell.empty_free_text(),
                            CompositeCell.empty_free_text(),
                            CompositeCell.empty_free_text(),
                            CompositeCell.free_text(
                                f'assays/{studyDbId}/datasets/phenotyping.csv')
                        ])

                    obs_to_add = [
                        observation
                        for _, row in group.iterrows()
                        for observation in data
                        if (
                            observation.observationUnitDbId == row['Assay Name'] and
                            observation.observationTimeStamp == row['Date'] and
                            observation.observationVariableDbId == row['Trait'] and
                            observation.value == row['Value']
                        )
                    ]
                    written_observations.extend(obs_to_add)

                    group = group.drop(columns=['Study'])
                    if not os.path.exists(f'data/assays/{studyDbId}/datasets'):
                        os.makedirs(f'data/assays/{studyDbId}/datasets')
                    if not os.path.exists(f'data/assays/{studyDbId}/datasets/phenotyping.csv'):
                        csv_action = 'create'
                        group.to_csv(
                            f'data/assays/{studyDbId}/datasets/phenotyping.csv', index=False)
                    else:
                        csv_action = 'update'
                        group.to_csv(
                            f'data/assays/{studyDbId}/datasets/phenotyping.csv', mode='a', header=False, index=False)

                    # TODO: If POST observations fails, do a git stash to revert the changes.
                    try:
                        assay.UpdateTable('Phenotyping', phenotyping)
                    except:
                        assay.AddTable(phenotyping)
                    spreadsheet = XlsxController().Assay().to_fs_workbook(assay)
                    Xlsx.to_xlsx_file(
                        f'data/assays/{studyDbId}/isa.assay.xlsx', spreadsheet)
                    actions.append(
                        {
                            'action': csv_action,
                            'file_path': f'assays/{studyDbId}/datasets/phenotyping.csv',
                            'encoding': 'base64',
                            'content': base64.b64encode(open(f'data/assays/{studyDbId}/datasets/phenotyping.csv', 'rb').read()).decode('utf-8')
                        }
                    )
                    actions.append(
                        {
                            'action': 'update',
                            'file_path': f'assays/{studyDbId}/isa.assay.xlsx',
                            'encoding': 'base64',
                            'content': base64.b64encode(open(f'data/assays/{studyDbId}/isa.assay.xlsx', 'rb').read()).decode('utf-8')
                        }
                    )
        json = {
            'branch': 'main',
            'commit_message': f'[brapi2arc] Add phenotyping data - {datetime.datetime.now()}',
            'actions': actions
        }
        response = requests.post(f'{os.getenv("DATAHUB_URL")}api/v4/projects/{os.getenv("ARC_URI").replace("/","%2F")}/repository/commits', headers={
            'PRIVATE-TOKEN': token
        }, json=json)
        response.raise_for_status()
        # FIXME: This is a workaround.
        # TODO: Race condition? What happens if multiple requests are made at the same time?
        for root, dirs, files in os.walk('data', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        git.Repo.clone_from(
            f"{os.getenv('DATAHUB_URL')}{os.getenv('ARC_URI')}", 'data')

        # TODO: Push to repo?
        arc_obj = arc.read('data')
        state.rocrate = JsonController().ARC().to_rocrate_json_string()(arc_obj)

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
                data=written_observations
            )
        )
