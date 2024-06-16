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
