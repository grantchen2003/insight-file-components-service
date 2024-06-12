import os, pymongo


class FileChunksDatabase:
    _collection = None

    @classmethod
    def _initialize_collection(cls) -> None:
        client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
        db = client[os.environ.get("MONGODB_DATABASE_NAME")]
        cls._collection = db["file_chunks"]

    @classmethod
    def get_sorted_file_chunks(cls, user_id: str, file_path: str, field: str):
        if cls._collection is None:
            FileChunksDatabase._initialize_collection()

        return cls._collection.find({"userid": user_id, "filepath": file_path}).sort(
            field, pymongo.ASCENDING
        )
