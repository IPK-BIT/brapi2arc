import warnings

from litestar import Litestar, get
from litestar.response import Redirect
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from routes.core.router import CoreRouter
from routes.germplasm.router import GermplasmRouter
from routes.phenotyping.router import PhenotypingRouter
from routes.search.router import SearchRouter
from dotenv import load_dotenv
import os
import git

from utils import arc

# IDEA: Maybe query the Gitlab for groups and their repsitories and list the groups as programs.
# This would allow this tool to be deployed for a DataHUB instead of a single ARC.
# e.g. ARC https://git.nfdi4plants.de/shape/spring and https://git.nfdi4plants.de/shape/winter would be in the program
# shape and contain the results for the spring and winter barley phenotyping results.
#
# TODO: How would the study type be determined?
# TODO: How would the ARC be stored?
# TODO: How to handle study/trial unspecific requests?

def init_app():
    load_dotenv()
    app.state.pat = os.getenv('DATAHUB_PAT')
    
    if not os.path.exists('data'):
        git.Repo.clone_from(f"{os.getenv('DATAHUB_URL')}{os.getenv('ARC_URI')}", 'data')

    metadata_path = 'data/metadata.json'
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as file:
            app.state.rocrate = file.read()
    else:
        warnings.warn(RuntimeWarning(
            'No metadata found. Trying to create a RO-Crate.json from ARC...'))
        arc_obj = arc.read('data')
        rocrate_json = arc.ARC().to_rocrate_json_string()(arc_obj)
        # FIXME: Needs manual intervention to convert the values to strings.
        with open(metadata_path, 'w') as file:
            file.write(rocrate_json)
        app.state.rocrate = rocrate_json

@get('/brapi/v2/serverinfo', include_in_schema=False)
async def server_info() -> dict:
    return {
        "metadata": {
            "datafiles": [],
            "pagination": {
            "currentPage": 0,
            "pageSize": 1000,
            "totalCount": 10,
            "totalPages": 1
            },
            "status": [
            {
                "message": "Request accepted, response successful",
                "messageType": "INFO"
            }
            ]
        },
        "result": {
            "calls": [
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "trials",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "programs",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "studies",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "studytypes",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "POST"
                ],
                "service": "search/germplasm",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "germplasm",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "POST"
                ],
                "service": "search/variables",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "observationunits",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "POST"
                ],
                "service": "observationunits",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "POST"
                ],
                "service": "observations",
                "versions": [
                    "2.1"
                ]
            },
            {
                "contentTypes": [
                    "application/json"
                ],
                "methods": [
                    "GET"
                ],
                "service": "variables",
                "versions": [
                    "2.1"
                ]
            }
            ],
            "contactEmail": "feser@ipk-gatersleben.de",
            "documentationURL": "",
            "location": "Germany",
            "organizationName": "IPK Gatersleben",
            "organizationURL": "leibniz-ipk.de",
            "serverDescription": "Brapi2ARC Test Server",
            "serverName": "The BrAPI 2 ARC Test Server"
        }
        }

@get('/', include_in_schema=False)
async def root() -> None:
    return Redirect('/schema')

cors_config = CORSConfig(
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_credentials=True
)

app = Litestar(
    route_handlers=[
        server_info,
        root,
        CoreRouter,
        GermplasmRouter,
        PhenotypingRouter,
        SearchRouter
    ],
    cors_config=cors_config,
    on_startup=[init_app],
    openapi_config=OpenAPIConfig(
        title='BrAPI 2 ARC',
        version='0.1.0',
        render_plugins=[ScalarRenderPlugin()]
    )
)
