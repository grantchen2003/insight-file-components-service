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
    def BatchExtractFileComponents(self, request, _):
        print("received BatchExtractFileComponents request")

        def extract_file_components(file_path: str):
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
                    user_id=request.user_id,
                    file_path=file_path,
                    start_line=file_component["start_line"],
                    end_line=file_component["end_line"],
                )
                for file_component in utils.extract_file_components(source_code)
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            file_components = utils.flatten_list(
                list(executor.map(extract_file_components, request.file_paths))
            )

        return file_components_service_pb2.FileComponents(
            file_components=file_components
        )

    def GetSavedFileComponents(self, request, _):
        print("received GetSavedFileComponents request")

        db = database.get_singleton_instance()

        saved_file_components = db.get_file_components(request.saved_file_component_ids)

        return file_components_service_pb2.SavedFileComponents(
            saved_file_components=saved_file_components
        )

    def SaveFileComponents(self, request, _):
        print("received SaveFileComponents request")

        file_components = [
            {
                "user_id": file_component.user_id,
                "file_path": file_component.file_path,
                "start_line": file_component.start_line,
                "end_line": file_component.end_line,
            }
            for file_component in request.file_components
        ]

        db = database.get_singleton_instance()

        saved_file_component_ids = db.save_file_components(file_components)
        
        print(saved_file_component_ids)

        return file_components_service_pb2.SavedFileComponentIds(
            saved_file_component_ids=saved_file_component_ids
        )
