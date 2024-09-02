from pydantic import BaseModel

from models.commons import Donor, ExternalReference, Origin, StorageType, Synonym, Taxon, Institute, CollectingInfo, DonorInfo


class Germplasm(BaseModel):
    accessionNumber: str | None = None
    acquisitionDate: str | None = None
    additionalInfo: dict | None = None
    biologicalStatusOfAccessionCode: str | None = None
    biologicalStatusOfAccessionDescription: str | None = None
    breedingMethodDbId: str | None = None
    breedingMethodName: str | None = None
    collection: str | None = None
    commonCropName: str | None = None
    countryOfOriginCode: str | None = None
    defaultDisplayName: str | None = None
    documentationURL: str | None = None
    donors: list[Donor] | None = None
    externalReferences: list[ExternalReference] | None = None
    genus: str | None = None
    germplasmDbId: str
    germplasmName: str | None = None
    germplasmOrigin: list[Origin] | None = None
    germplasmPUI: str | None = None
    germplasmPreprocessing: str | None = None
    instituteCode: str | None = None
    instituteName: str | None = None
    pedigree: str | None = None
    seedSource: str | None = None
    seedSourceDescription: str | None = None
    species: str | None = None
    speciesAuthority: str | None = None
    storageTypes: list[StorageType] | None = None
    subtaxa: str | None = None
    subtaxaAuthority: str | None = None
    synonyms: list[Synonym] | None = None
    taxonIds: list[Taxon] | None = None
