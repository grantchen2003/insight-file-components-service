import concurrent.futures

from file_components_service.protobufs import (
    file_components_service_pb2,
    file_components_service_pb2_grpc,
)
from file_components_service import utils
from file_components_service.services import file_chunks_service


class FileSegment(file_components_service_pb2_grpc.FileComponentsServiceServicer):
    def ExtractStructure(self, request, context):
        print("ExtractStructure request received")

        def extract_file_segments(file_path):
            sorted_file_chunks_content = file_chunks_service.get_sorted_file_chunks_content(
                request.user_id, file_path
            )
            
            source_code = "".join(sorted_file_chunks_content)
            
            print(source_code)

            return [
                file_components_service_pb2.FileComponent(
                    file_path=file_path,
                    start_line=file_segment["start_line"],
                    end_line=file_segment["end_line"],
                )
                for file_segment in utils.extract_file_structure(source_code)
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for file_segments in executor.map(
                extract_file_segments, request.file_paths
            ):
                for file_segment in file_segments:
                    yield file_segment
