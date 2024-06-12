import concurrent, grpc, os

from file_segment_service.protobufs import file_segment_service_pb2_grpc
from file_segment_service.services import FileSegment


def start():
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(),
        options=[("grpc.max_receive_message_length", -1)],
    )

    file_segment_service_pb2_grpc.add_FileSegmentServiceServicer_to_server(
        FileSegment(), server
    )

    address = f"{os.environ['DOMAIN']}:{os.environ['PORT']}"
    server.add_insecure_port(address)
    print(f"starting file structure server on {address}")
    server.start()
    server.wait_for_termination()
