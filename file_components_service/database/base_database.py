from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def save_file_components(self, file_components: list[dict]) -> list[int]:
        pass

    @abstractmethod
    def get_file_components(self, file_component_ids: list[int]) -> list[dict]:
        pass

    @abstractmethod
    def delete_file_components_by_repository_id(self, repository_id: str) -> None:
        pass
    
    @abstractmethod
    def delete_file_components_by_repository_id_and_file_paths(self, repository_id: str, file_paths: list[str]) -> list[int]:
        pass