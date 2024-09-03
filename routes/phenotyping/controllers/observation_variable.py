from icecream import ic

from litestar import Controller, get
from litestar.datastructures import State
from arctrl.arctrl import JsonController
import pandas as pd
import os
import json

from models.response import Response, Metadata, Pagination, Result, Message, MESSAGETYPE
from models.phenotyping import ObservationVariable, Trait, Method, Scale, ScaleValues, ScaleValue

class ObservationVariableController(Controller):
    path = '/variables'

    @get('/')
    async def get_observation_variables(self, state: State, observationVariableName: str|None = None) -> Response[ObservationVariable]:
        isa = json.loads(JsonController.Investigation().to_isajson_string(
            JsonController.ARC().from_rocrate_json_string(state.rocrate).ISA
        ))

        filtered_variables = []
        for study in isa['studies']:
            tdf = pd.read_csv(os.path.join(
                'data/studies', study['identifier'], 'tdf.tsv'), sep='\t')
            for row in tdf.iterrows():
                if observationVariableName is None or row[1]['Variable Name'] in observationVariableName.split(','):
                    validValues = None
                    if row[1]['Scale Type'] in ['Nominal', 'Ordinal']:
                        validValues = ScaleValues(
                            categories=[ScaleValue(value=value.split(':')[0], label=value.split(':')[1]) for value in row[1]['Scale Values'].split(';')]
                        )
                    variable = ObservationVariable(
                        observationVariableDbId=row[1]['Variable ID'],
                        observationVariableName=row[1]['Variable Name'],
                        trait=Trait(
                            traitDbId=row[1]['Trait'],
                            traitName=row[1]['Trait'],
                            traitPUI=None if pd.isna(row[1]['Trait Accession Number']) else row[1]['Trait Accession Number'],
                        ),
                        method=Method(
                            methodDbId=row[1]['Method'],
                            methodName=row[1]['Method'],
                            methodPUI= None if pd.isna(row[1]['Method Accession Number']) else row[1]['Method Accession Number'],
                            description=row[1]['Method Description']
                        ),
                        scale=Scale(
                            dataType=row[1]['Scale Type'],
                            scaleDbId=row[1]['Scale'],
                            scaleName=row[1]['Scale'],
                            scalePUI= None if pd.isna(row[1]['Scale Accession Number']) else row[1]['Scale Accession Number'],
                            datatype=row[1]['Scale Type'],
                            validValues=validValues
                        )
                    )
                    if variable not in filtered_variables:
                        filtered_variables.append(variable)

        return Response(
            metadata=Metadata(
                pagination=Pagination(
                    currentPage=0,
                    pageSize=1000,
                    totalCount=len(filtered_variables),
                    totalPages=len(filtered_variables) // 1000 +
                    (1 if len(filtered_variables) % 1000 > 0 else 0)
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
                data=filtered_variables
            )
        )
