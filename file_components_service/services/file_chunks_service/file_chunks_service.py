import grpc, os

from .pb import file_chunks_service_pb2, file_chunks_service_pb2_grpc


def get_sorted_file_chunks_content(repository_id: str, file_path: str) -> list[bytes]:
    file_chunks_service_address = os.environ.get("FILE_CHUNKS_SERVICE_ADDRESS")

    with grpc.insecure_channel(file_chunks_service_address) as channel:
        stub = file_chunks_service_pb2_grpc.FileChunksServiceStub(channel)

        request = file_chunks_service_pb2.GetSortedFileChunksContentRequest(
            repository_id=repository_id, file_path=file_path
        )

        response = stub.GetSortedFileChunksContent(request)

        return [
            file_chunk_content.content
            for file_chunk_content in response.file_chunks_content
        ]
