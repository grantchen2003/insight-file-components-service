from file_structure_service.protobufs import (
    file_structure_service_pb2_grpc,
    file_structure_service_pb2,
)

from file_structure_service.database import FileChunksDatabase


class FileStructure(file_structure_service_pb2_grpc.FileStructureServiceServicer):
    def ExtractStructure(self, requests, context):
        print("ExtractStructure request received")
        for request in requests:
            print(request.user_id, request.file_path)
            
            file_chunks = FileChunksDatabase.get_file_chunks(request.user_id, request.file_path)
            
            for file_chunk in file_chunks:
                print(file_chunk)
                
            # why should it be stream vs repeated in proto file
            
            # with repeated (i can make 1 massive request to db)
            
            # but what if request is too big, batch again ? (use the fact the documents themselves r alr somewhat batched)
            # fetch file from db (note that they are in chunks lmfao)
            
            # parse it
            
            # return parsed blocks to client
            response = file_structure_service_pb2.FileStructure()
            yield response
