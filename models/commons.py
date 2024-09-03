from pydantic import BaseModel


class ExternalReference(BaseModel):
    referenceID: str | None = None
    referenceSource: str | None = None


class DocumentationLink(BaseModel):
    URL: str | None = None
    type: str | None = None


class OntologyReference(BaseModel):
    documentationLinks: list[DocumentationLink] | None = None
    ontologyDbId: str | None = None
    ontologyName: str | None = None
    version: str | None = None


class ScaleValue(BaseModel):
    label: str | None = None
    value: str | None = None


class ScaleValues(BaseModel):
    categories: list[ScaleValue] | None = None
    maximumValue: str | None = None
    minimumValue: str | None = None


class Contact(BaseModel):
    contactDbId: str | None = None
    email: str | None = None
    institutionName: str | None = None
    name: str | None = None
    orcid: str | None = None
    type: str | None = None


class Dataset(BaseModel):
    datasetPUI: str | None = None
    license: str | None = None
    publicReleaseDate: str | None = None
    submissionDate: str | None = None


class Publication(BaseModel):
    publicationPUI: str | None = None
    publicationReference: str | None = None


class DataLink(BaseModel):
    dataFormat: str | None = None
    description: str | None = None
    fileFormat: str | None = None
    name: str | None = None
    provenance: str | None = None
    scientificType: str | None = None
    url: str | None = None
    version: str | None = None


class EnvironmentParameter(BaseModel):
    description: str | None = None
    parameterName: str | None = None
    parameterPUI: str | None = None
    unit: str | None = None
    unitPUI: str | None = None
    value: str | None = None
    valuePUI: str | None = None


class ExperimentalDesign(BaseModel):
    description: str | None = None
    PUI: str | None = None


class GrowthFacility(BaseModel):
    description: str | None = None
    PUI: str | None = None


class Update(BaseModel):
    timestamp: str | None = None
    version: str | None = None


class ObservationLevel(BaseModel):
    levelCode: str | None = None
    levelName: str | None = None
    levelOrder: int | None = None


class Donor(BaseModel):
    donorAccessionNumber: str | None = None
    donorInstituteCode: str | None = None


class Geometry(BaseModel):
    coordinates: list[float] | None = None
    type: str | None = None


class Coordinate(BaseModel):
    geometry: Geometry | None = None
    type: str | None = None


class Origin(BaseModel):
    coordinatesUncertainty: str | None = None
    coordinates: Coordinate | None = None


class StorageType(BaseModel):
    code: str | None = None
    description: str | None = None


class Synonym(BaseModel):
    synonym: str | None = None
    type: str | None = None


class Taxon(BaseModel):
    sourceName: str | None = None
    taxonId: str | None = None


class Institute(BaseModel):
    instituteCode: str | None = None
    instituteName: str | None = None


class CollectingInsitute(Institute):
    instituteAddress: str | None = None


class CollectingSite(BaseModel):
    coordinateUncertainty: str | None = None
    elevation: str | None = None
    georeferencingMethod: str | None = None
    latitudeDecimal: str | None = None
    latitudeDegrees: str | None = None
    locationDescription: str | None = None
    longitudeDecimal: str | None = None
    longitudeDegrees: str | None = None
    spatialReferenceSystem: str | None = None


class CollectingInfo(BaseModel):
    collectingDate: str | None = None
    collectingInstitute: CollectingInsitute | None = None
    collectingMissionIdentifier: str | None = None
    collectingNumber: str | None = None
    collectingSite: CollectingSite | None = None


class DonorInfo(BaseModel):
    donorAccessionNumber: str | None = None
    donorAccessionPui: str | None = None
    donorInstitute: Institute | None = None


class Season(BaseModel):
    seasonDbId: str | None = None
    season: str | None = None
    year: int | None = None


class ObservationLevelRelation(BaseModel):
    leveCode: str | None = None
    levelName: str | None = None
    levelOrder: int | None = None


class Position(BaseModel):
    entryType: str | None = None
    geoCoordinates: Coordinate | None = None
    observationLevel: ObservationLevel | None = None
    observationLevelRelationships: list[ObservationLevelRelation] | None = None
    positionCoordinateX: str | None = None
    positionCoordinateXType: str | None = None
    positionCoordinateY: str | None = None
    positionCoordinateYType: str | None = None


class Treatment(BaseModel):
    factor: str | None = None
    modality: str | None = None
