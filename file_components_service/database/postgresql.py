from file_components_service.database.base_database import FileComponent
from .base_database import BaseDatabase


class PostgreSql(BaseDatabase):
    def save_file_components(self, file_components: list[FileComponent]) -> list[str]:
        file_components_ids = ["sadfasfa" for _ in file_components]
        return file_components_ids
