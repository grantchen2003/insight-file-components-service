import concurrent.futures

from file_components_service import database, utils
from file_components_service.services import file_chunks_service
from file_components_service.protobufs import (
    file_components_service_pb2,
    file_components_service_pb2_grpc,
)


class FileComponentServicer(
    file_components_service_pb2_grpc.FileComponentsServiceServicer
):
    def GetSavedFileComponents(self, request, _):
        print("received GetFileComponents request")

        db = database.get_singleton_instance()

        saved_file_components = db.get_file_components(request.file_component_ids)

        return file_components_service_pb2.GetSavedFileComponentsResponse(
            saved_file_components=saved_file_components
        )

    def SaveFileComponents(self, request, _):
        print("received SaveFileComponents request")

        file_components = [
            {
                "user_id": request.user_id,
                "file_path": file_component.file_path,
                "start_line": file_component.start_line,
                "end_line": file_component.end_line,
            }
            for file_component in request.file_components
        ]

        db = database.get_singleton_instance()

        file_component_ids = db.save_file_components(file_components)

        print(file_component_ids)

        return file_components_service_pb2.SaveFileComponentsResponse(
            file_component_ids=file_component_ids
        )

    def ExtractFilesComponents(self, request, _):
        print("received ExtractFilesComponents request")

        def extract_file_components(
            file_path: str,
        ) -> list[file_components_service_pb2.FileComponent]:
            sorted_file_chunks_content = (
                file_chunks_service.get_sorted_file_chunks_content(
                    request.user_id, file_path
                )
            )

            source_code = "".join(
                file_chunk_content.decode("utf-8")
                for file_chunk_content in sorted_file_chunks_content
            )

            return [
                file_components_service_pb2.FileComponent(
                    file_path=file_path,
                    start_line=file_component["start_line"],
                    end_line=file_component["end_line"],
                )
                for file_component in utils.extract_file_components(source_code)
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for file_components in executor.map(
                extract_file_components, request.file_paths
            ):
                for file_component in file_components:
                    yield file_component