import os, psycopg2

from .base_database import BaseDatabase


class PostgreSql(BaseDatabase):
    def __init__(self):
        self._connection = None
        self._cursor = None

    def _ensure_connection(self):
        if self._connection is None or self._connection.closed != 0:
            self.connect()

    def connect(self) -> None:
        self._connection = psycopg2.connect(
            dbname=os.environ["POSTGRESQL_DATABASE_NAME"],
            user=os.environ["POSTGRESQL_USERNAME"],
            password=os.environ["POSTGRESQL_PASSWORD"],
            host=os.environ["POSTGRESQL_HOST"],
            port=os.environ["POSTGRESQL_PORT"],
        )
        self._cursor = self._connection.cursor()
        print("connected to PostgreSql")

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()

    def get_file_components(self, file_component_ids: list[int]) -> list[dict]:
        if not file_component_ids:
            return []

        self._ensure_connection()

        file_component_ids_str = ",".join(str(id) for id in file_component_ids)

        select_query = (
            f"SELECT * FROM file_components WHERE id IN ({file_component_ids_str});"
        )

        self._cursor.execute(select_query)

        file_components = [
            {
                "id": id,
                "repository_id": repository_id,
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "content": content,
            }
            for id, repository_id, file_path, start_line, end_line, content in self._cursor.fetchall()
        ]

        return file_components

    def save_file_components(self, file_components: list[dict]) -> list[dict]:
        if not file_components:
            return []

        self._ensure_connection()
        
        self._ensure_file_components_table_exists()

        file_component_tuples = [
            (
                file_component["repository_id"],
                file_component["file_path"],
                file_component["start_line"],
                file_component["end_line"],
                file_component["content"],
            )
            for file_component in file_components
        ]

        args = ",".join(
            self._cursor.mogrify("(%s,%s,%s,%s,%s)", file_component_tuple).decode(
                "utf-8"
            )
            for file_component_tuple in file_component_tuples
        )

        query = f"INSERT INTO file_components(repository_id, file_path, start_line, end_line, content)  VALUES {args} RETURNING id, repository_id, file_path, start_line, end_line, content;"

        self._cursor.execute(query)

        inserted_file_components = [
            {
                "id": id,
                "repository_id": repository_id,
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "content": content,
            }
            for id, repository_id, file_path, start_line, end_line, content in self._cursor.fetchall()
        ]

        self._connection.commit()

        return inserted_file_components

    def delete_file_components_by_repository_id(self, repository_id: str) -> None:
        self._ensure_connection()

        query = "DELETE FROM file_components WHERE repository_id = %s"

        self._cursor.execute(query, (repository_id,))

        self._connection.commit()

    def delete_file_components_by_repository_id_and_file_paths(
        self, repository_id: str, file_paths: list[str]
    ) -> list[int]:
        self._ensure_connection()

        query = "DELETE FROM file_components WHERE repository_id = %s AND file_path IN %s RETURNING id"

        self._cursor.execute(query, (repository_id, tuple(file_paths)))

        deleted_ids = [row[0] for row in self._cursor.fetchall()]
        self._connection.commit()

        return deleted_ids

    def _ensure_file_components_table_exists(self) -> None:
        self._ensure_connection()

        create_file_components_table_query = """
            CREATE TABLE IF NOT EXISTS file_components (
                id SERIAL PRIMARY KEY,
                repository_id VARCHAR(255),
                file_path VARCHAR(255),
                start_line INT,
                end_line INT,
                content text
            );
        """
        self._cursor.execute(create_file_components_table_query)
        self._connection.commit()
