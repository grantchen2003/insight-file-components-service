import os

from file_components_service import config, database, server


def main() -> None:
    env = os.environ.get("ENV")
    config.load_env_vars(env)
    print(f"ENV={env}")

    db = database.get_singleton_instance()
    db.connect()

    server.start()


if __name__ == "__main__":
    main()
