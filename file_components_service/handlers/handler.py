import concurrent.futures, functools, logging

from google.protobuf import empty_pb2

from file_components_service import database, utils
from file_components_service.protobufs import (
    file_components_service_pb2,
    file_components_service_pb2_grpc,
)
from file_components_service.services import file_chunks_service


# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def log_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper


class FileComponentServicer(
    file_components_service_pb2_grpc.FileComponentsServiceServicer
):
    @log_error
    def CreateFileComponents(self, request, _):
        logger.info("received CreateFileComponents request")

        def extract_file_components(file_path: str):
            sorted_file_chunks_content = (
                file_chunks_service.get_sorted_file_chunks_content(
                    request.repository_id, file_path
                )
            )

            source_code = "".join(
                file_chunk_content.decode("utf-8")
                for file_chunk_content in sorted_file_chunks_content
            )

            file_component_content_and_lines = (
                utils.extract_file_component_content_and_lines(source_code)
            )

            return [
                {
                    "repository_id": request.repository_id,
                    "file_path": file_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "content": content,
                }
                for start_line, end_line, content in file_component_content_and_lines
            ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            file_components = utils.flatten_list(
                list(executor.map(extract_file_components, request.file_paths))
            )

        db = database.get_singleton_instance()

        file_components = db.save_file_components(file_components)

        for file_component in file_components:
            yield file_components_service_pb2.FileComponent(**file_component)

    @log_error
    def GetFileComponents(self, request, _):
        logger.info("received GetFileComponents request")

        db = database.get_singleton_instance()

        file_components = db.get_file_components(request.file_component_ids)

        for file_component in file_components:
            yield file_components_service_pb2.FileComponent(**file_component)

    @log_error
    def DeleteFileComponentsByRepositoryId(self, request, _):
        logger.info("received DeleteFileComponentsByRepositoryId request")

        db = database.get_singleton_instance()

        db.delete_file_components_by_repository_id(request.repository_id)

        return empty_pb2.Empty()

    @log_error
    def DeleteFileComponentsByRepositoryIdAndFilePaths(self, request, _):
        logger.info("received DeleteFileComponentsByRepositoryIdAndFilePaths request")

        db = database.get_singleton_instance()

        file_component_ids = db.delete_file_components_by_repository_id_and_file_paths(
            request.repository_id, request.file_paths
        )

        return file_components_service_pb2.FileComponentIds(
            file_component_ids=file_component_ids
        )
