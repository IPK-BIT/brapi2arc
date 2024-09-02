from pydantic import BaseModel

from models.commons import ExternalReference, Contact, DataLink, Dataset, Publication, DataLink, EnvironmentParameter, ExperimentalDesign, GrowthFacility, ObservationLevel, Update


class Program(BaseModel):
    abbreviation: str | None = None
    additionalInfo: dict | None = None
    commonCropName: str | None = None
    documentationURL: str | None = None
    externalReferences: list[ExternalReference] | None = None
    fundingInstitutions: str | None = None
    leadPersonDbId: str | None = None
    leadPersonName: str | None = None
    objective: str | None = None
    programDbId: str
    programName: str | None = None
    programType: str | None = None


class Trial(BaseModel):
    active: bool | None = None
    additionalInfo: dict | None = None
    commonCropName: str | None = None
    contacts: list[Contact] | None = None
    datasetAuthorships: list[Dataset] | None = None
    documentationURL: str | None = None
    endDate: str | None = None
    externalReferences: list[ExternalReference] | None = None
    programDbId: str | None = None
    programName: str | None = None
    publications: list[Publication] | None = None
    startDate: str | None = None
    trialDbId: str
    trialDescription: str | None = None
    trialName: str | None = None
    trialPUI: str | None = None


class Study(BaseModel):
    active: bool | None = None
    additionalInfo: dict | None = None
    commonCropName: str | None = None
    contacts: list[Contact] | None = None
    culturalPractices: str | None = None
    dataLinks: list[DataLink] | None = None
    documentationURL: str | None = None
    endDate: str | None = None
    environmentParameters: list[EnvironmentParameter] | None = None
    experimentalDesign: ExperimentalDesign | None = None
    externalReferences: list[ExternalReference] | None = None
    growthFacility: GrowthFacility | None = None
    lastUpdate: Update | None = None
    license: str | None = None
    locationDbId: str | None = None
    locationName: str | None = None
    observationLevels: list[ObservationLevel] | None = None
    observationUnitsDescription: str | None = None
    observationVariableDbIds: list[str] | None = None
    seasons: list[str] | None = None
    startDate: str | None = None
    studyCode: str | None = None
    studyDbId: str
    studyDescription: str | None = None
    studyName: str | None = None
    studyPUI: str | None = None
    studyType: str | None = None
    trialDbId: str | None = None
    trialName: str | None = None
