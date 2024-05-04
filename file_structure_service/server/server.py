import concurrent, grpc, os

from file_structure_service.protobufs import file_structure_service_pb2_grpc
from file_structure_service.services import FileStructure


def start():
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(),
        options=[("grpc.max_receive_message_length", -1)],
    )

    file_structure_service_pb2_grpc.add_FileStructureServiceServicer_to_server(
        FileStructure(), server
    )

    address = f"{os.environ['DOMAIN']}:{os.environ['PORT']}"
    server.add_insecure_port(address)
    print(f"starting file structure server on {address}")
    server.start()
    server.wait_for_termination()
