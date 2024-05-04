from file_structure_service.protobufs import (
    file_structure_service_pb2_grpc,
    file_structure_service_pb2,
)


class FileStructure(file_structure_service_pb2_grpc.FileStructureServiceServicer):
    def ExtractStructure(self, requests, context):
        print("ExtractStructure request received")
        for request in requests:
            print(request.user_id, request.file_path)

        # files = [
        #     {"user_id": request.user_id, "file_path": request.file_path}
        #     for request in requests
        # ]

        # print(files)

        for i in range(6):
            print(i)
            response = file_structure_service_pb2.FileStructure(
                blocks=[], classes=[], methods=[]
            )
            yield response
