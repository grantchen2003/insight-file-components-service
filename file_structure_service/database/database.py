from pymongo import MongoClient
import os


class FileChunksDatabase:
    _client = None 
    _db = None
    _collection = None
    
    @classmethod
    def initialize(cls) -> None:
        cls._client = MongoClient(os.environ.get("MONGODB_URI"))
        cls._db = cls._client[os.environ.get("MONGODB_DATABASE_NAME")]
        cls._collection = cls._db["file_chunks"]
        
    @classmethod
    def get_file_chunks(cls, user_id: str, file_path: str):
        return cls._collection.find({
            "userid": user_id,
            "filepath": file_path
        })