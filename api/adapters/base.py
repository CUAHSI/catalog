import abc

from api.config import Settings, get_settings
from api.models.catalog import DatasetMetadataDOC


class AbstractRepositoryRequestHandler(abc.ABC):
    settings: Settings = get_settings()

    @abc.abstractmethod
    def get_metadata(self, record_id: str):
        """Returns the metadata for the specified record from a repository"""
        ...


class AbstractRepositoryMetadataAdapter(abc.ABC):
    repo_api_handler: AbstractRepositoryRequestHandler

    @staticmethod
    @abc.abstractmethod
    def to_catalog_record(metadata: dict) -> DatasetMetadataDOC:
        """Converts repository metadata to a catalog dataset record"""
        ...

    @staticmethod
    @abc.abstractmethod
    def to_repository_record(catalog_record: DatasetMetadataDOC):
        """Converts dataset catalog dataset record to repository metadata"""
        ...

    async def get_metadata(self, record_id: str):
        """Returns the metadata for the specified record from a repository"""

        return self.repo_api_handler.get_metadata(record_id)
