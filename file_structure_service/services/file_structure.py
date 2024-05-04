from file_structure_service.protobufs import (
    file_structure_service_pb2_grpc,
    file_structure_service_pb2,
)


class FileStructure(file_structure_service_pb2_grpc.FileStructureServiceServicer):
    def ExtractStructure(self, requests, context):
        print("ExtractStructure request received")
        for request in requests:
            print(request.user_id, request.file_path)
            # fetch file from db (note that they are in chunks lmfao)
            
            # parse it
            
            # return parsed blocks to client
            print(request.user_id, request.file_path)
            response = file_structure_service_pb2.FileStructure(
                blocks=[], classes=[], methods=[]
            )
            yield response
