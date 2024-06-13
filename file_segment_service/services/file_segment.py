import base64, concurrent.futures

from file_segment_service.protobufs import (
    file_segment_service_pb2,
    file_segment_service_pb2_grpc,
)
from file_segment_service.database import FileChunksDatabase
from file_segment_service import utils


class FileSegment(file_segment_service_pb2_grpc.FileSegmentServiceServicer):
    def ExtractStructure(self, request, context):
        print("ExtractStructure request received")

        def extract_file_segments(file_path):
            sorted_file_chunks = FileChunksDatabase.get_sorted_file_chunks(
                request.user_id, file_path, "contentchunkindex"
            )

            decoded_contents = [
                base64.b64decode(file_chunk["content"]).decode("utf-8")
                for file_chunk in sorted_file_chunks
            ]

            source_code = "".join(decoded_contents)

            return [
                file_segment_service_pb2.FileSegment(
                    file_path=file_path,
                    start_line=file_segment["start_line"],
                    end_line=file_segment["end_line"],
                )
                for file_segment in utils.extract_file_structure(source_code)
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for file_segments in executor.map(extract_file_segments, request.file_paths):
                for file_segment in file_segments:
                    yield file_segment
