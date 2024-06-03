import base64

from file_structure_service.protobufs import (
    file_structure_service_pb2_grpc,
    file_structure_service_pb2,
)

from file_structure_service.database import FileChunksDatabase


class FileStructure(file_structure_service_pb2_grpc.FileStructureServiceServicer):
    def ExtractStructure(self, request, context):
        print("ExtractStructure request received")
        
        user_id = request.user_id
        file_paths = request.file_paths
        
        print(user_id, file_paths)
        
        for file_path in file_paths:
            # print(request.user_id, request.file_path)
            
            # file_chunks = FileChunksDatabase.get_file_chunks(request.user_id, request.file_path)
            
            # file_content = ""
            
            # sorted_file_chunks = sorted(file_chunks, key = lambda file_chunk: file_chunk["contentchunkindex"])
            # decoded_contents = [base64.b64decode(file_chunk["content"]).decode("utf-8") for file_chunk in sorted_file_chunks]
            # file_content = "".join(decoded_contents)
            
            # print(file_content)
            
                
            # why should it be stream vs repeated in proto file
            
            # with repeated (i can make 1 massive request to db)
            
            # but what if request is too big, batch again ? (use the fact the documents themselves r alr somewhat batched)
            # fetch file from db (note that they are in chunks lmfao)
            
            # parse it
            
            # return parsed blocks to client
            response = file_structure_service_pb2.FileStructure(file_path=file_path)
            yield response
