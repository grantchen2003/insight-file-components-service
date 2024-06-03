from pymongo import MongoClient
import os


class FileChunksDatabase:
    _collection = None
    
    @classmethod
    def _initialize_collection(cls) -> None:
        client = MongoClient(os.environ.get("MONGODB_URI"))
        db = client[os.environ.get("MONGODB_DATABASE_NAME")]
        cls._collection = db["file_chunks"]
        
    @classmethod
    def get_file_chunks(cls, user_id: str, file_path: str):
        if cls._collection is None:
            FileChunksDatabase._initialize_collection()
            
        return cls._collection.find({
            "userid": user_id,
            "filepath": file_path
        })