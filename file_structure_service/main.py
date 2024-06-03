from file_structure_service import config, server
from file_structure_service.database import FileChunksDatabase


def main() -> None:
    config.load_env_var()
    server.start()


if __name__ == "__main__":
    main()
