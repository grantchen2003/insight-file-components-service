import concurrent, grpc, os

from file_components_service.handlers import FileComponentServicer
from file_components_service.protobufs import file_components_service_pb2_grpc


def start() -> None:
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(),
        options=[("grpc.max_receive_message_length", -1)],
    )

    file_components_service_pb2_grpc.add_FileComponentsServiceServicer_to_server(
        FileComponentServicer(), server
    )

    address = f"{os.environ['DOMAIN']}:{os.environ['PORT']}"
    server.add_insecure_port(address)
    print(f"starting file structure server on {address}")
    server.start()
    server.wait_for_termination()
