import base64

from file_segment_service.protobufs import (
    file_segment_service_pb2,
    file_segment_service_pb2_grpc,
)

from file_segment_service.database import FileChunksDatabase
from file_segment_service import utils


class FileSegment(file_segment_service_pb2_grpc.FileSegmentServiceServicer):
    def ExtractStructure(self, request, context):
        print("ExtractStructure request received")

        user_id = request.user_id
        file_paths = request.file_paths

        print(user_id, file_paths)

        for file_path in file_paths:
            file_chunks = FileChunksDatabase.get_file_chunks(
                request.user_id, request.file_path
            )

            sorted_file_chunks = sorted(
                file_chunks, key=lambda file_chunk: file_chunk["contentchunkindex"]
            )

            decoded_contents = [
                base64.b64decode(file_chunk["content"]).decode("utf-8")
                for file_chunk in sorted_file_chunks
            ]

            source_code = "".join(decoded_contents)

            for file_segment in utils.extract_file_structure(source_code):
                yield file_segment_service_pb2.FileSegment(
                    file_path=file_path,
                    start_line=file_segment["start_line"],
                    end_line=file_segment["end_line"],
                )

            # print(file_content)

            # why should it be stream vs repeated in proto file

            # with repeated (i can make 1 massive request to db)

            # but what if request is too big, batch again ? (use the fact the documents themselves r alr somewhat batched)
            # fetch file from db (note that they are in chunks lmfao)

            # parse it

            # return parsed blocks to client
