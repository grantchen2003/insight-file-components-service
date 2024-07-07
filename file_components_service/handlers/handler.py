import concurrent.futures

from file_components_service import database, utils
from file_components_service.protobufs import (
    file_components_service_pb2,
    file_components_service_pb2_grpc,
)
from file_components_service.services import file_chunks_service


class FileComponentServicer(
    file_components_service_pb2_grpc.FileComponentsServiceServicer
):
    def CreateFileComponents(self, request, _):
        print("received CreateFileComponents request")

        def extract_file_components(file_path: str):
            sorted_file_chunks_content = (
                file_chunks_service.get_sorted_file_chunks_content(
                    request.repository_id, file_path
                )
            )

            source_code = "".join(
                file_chunk_content.decode("utf-8")
                for file_chunk_content in sorted_file_chunks_content
            )

            file_component_content_and_lines = (
                utils.extract_file_component_content_and_lines(source_code)
            )

            return [
                {
                    "repository_id": request.repository_id,
                    "file_path": file_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "content": content,
                }
                for start_line, end_line, content in file_component_content_and_lines
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            file_components = utils.flatten_list(
                list(executor.map(extract_file_components, request.file_paths))
            )

        db = database.get_singleton_instance()

        file_components = db.save_file_components(file_components)

        pb_file_components = [
            file_components_service_pb2.FileComponent(**file_component)
            for file_component in file_components
        ]

        return file_components_service_pb2.FileComponents(
            file_components=pb_file_components
        )

    def GetFileComponents(self, request, _):
        print("received GetFileComponents request")

        db = database.get_singleton_instance()

        file_components = db.get_file_components(request.file_component_ids)

        return file_components_service_pb2.FileComponents(
            file_components=file_components
        )
