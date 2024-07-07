import os, psycopg2

from .base_database import BaseDatabase


class PostgreSql(BaseDatabase):
    def __init__(self):
        self._connection = None
        self._cursor = None

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

    def _ensure_file_components_table_exists(self) -> None:
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
