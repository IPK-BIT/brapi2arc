from pydantic import BaseModel

from models.commons import ExternalReference, OntologyReference, ScaleValues, Season, Position, Treatment, ScaleValue, Coordinate, ObservationLevel


class Method(BaseModel):
    additionalInfo: dict | None = None
    bibliographicalReference: str | None = None
    description: str | None = None
    externalReferences: list[ExternalReference] | None = None
    formula: str | None = None
    methodClass: str | None = None
    methodDbId: str | None = None
    methodName: str | None = None
    methodPUI: str | None = None
    ontologyReference: OntologyReference | None = None


class Scale(BaseModel):
    additionalInfo: dict | None = None
    dataType: str | None = None
    decimalPlaces: int | None = None
    externalReferences: list[ExternalReference] | None = None
    ontologyReference: OntologyReference | None = None
    scaleDbId: str | None = None
    scaleName: str | None = None
    scalePUI: str | None = None
    units: str | None = None
    validValues: ScaleValues | None = None


class Trait(BaseModel):
    additionalInfo: dict | None = None
    alternativeAbbreviations: list[str] | None = None
    attribute: str | None = None
    attributePUI: str | None = None
    entity: str | None = None
    entityPUI: str | None = None
    externalReferences: list[ExternalReference] | None = None
    mainAbbreviation: str | None = None
    ontologyReference: OntologyReference | None = None
    status: str | None = None
    synonyms: list[str] | None = None
    traitClass: str | None = None
    traitDbId: str | None = None
    traitDescription: str | None = None
    traitName: str | None = None
    traitPUI: str | None = None


class ObservationVariable(BaseModel):
    additionalInfo: dict | None = None
    commonCropName: str | None = None
    contextOfUse: list[str] | None = None
    defaultValue: str | None = None
    documentationURL: str | None = None
    externalReferences: list[ExternalReference] | None = None
    growthStage: str | None = None
    institution: str | None = None
    language: str | None = None
    method: Method | None = None
    observationVariableDbId: str | None = None
    observationVariableName: str | None = None
    observationVariablePUI: str | None = None
    ontologyReference: OntologyReference | None = None
    scale: Scale | None = None
    scientist: str | None = None
    status: str | None = None
    submissionTimestamp: str | None = None
    synonyms: list[str] | None = None
    trait: Trait | None = None


class Observation(BaseModel):
    additionalInfo: dict | None = None
    collector: str | None = None
    externalReferences: list[ExternalReference] | None = None
    geoCoordinates: Coordinate | None = None
    germplasmDbId: str | None = None
    germplasmName: str | None = None
    observationDbId: str | None = None
    observationTimeStamp: str | None = None
    observationUnitDbId: str | None = None
    observationUnitName: str | None = None
    observationVariableDbId: str | None = None
    observationVariableName: str | None = None
    season: list[Season] | None = None
    studyDbId: str | None = None
    studyName: str | None = None
    uploadedBy: str | None = None
    value: str | None = None


class ObservationUnit(BaseModel):
    additionalInfo: dict | None = None
    crossDbId: str | None = None
    crossName: str | None = None
    externalReferences: list[ExternalReference] | None = None
    germplasmDbId: str | None = None
    germplasmName: str | None = None
    locationDbId: str | None = None
    locationName: str | None = None
    observationUnitDbId: str | None = None
    observationUnitName: str | None = None
    observationUnitPUI: str | None = None
    observationUnitPosition: Position | None = None
    observations: list[Observation] | None = None
    programDbId: str | None = None
    programName: str | None = None
    seedLotDbId: str | None = None
    seedLotName: str | None = None
    studyDbId: str | None = None
    studyName: str | None = None
    treatments: list[Treatment] | None = None
    trialDbId: str | None = None
    trialName: str | None = None
