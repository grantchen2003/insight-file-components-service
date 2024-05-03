from file_structure_service import config, server


def main() -> None:
    config.load_env_var()
    server.start()


if __name__ == "__main__":
    main()
