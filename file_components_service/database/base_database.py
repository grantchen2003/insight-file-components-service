from abc import ABC, abstractmethod
from typing import TypedDict


class FileComponent(TypedDict):
    user_id: str
    file_path: str
    start_line: int
    end_line: int


class BaseDatabase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def save_file_components(self, file_components: list[FileComponent]) -> list[int]:
        pass
