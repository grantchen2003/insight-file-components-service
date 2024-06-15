import os
from dotenv import load_dotenv

__ENV_FILES = {
    "dev": ".env.dev",
    "prod": ".env.prod",
}


def load_env_var():
    env = os.environ.get("ENV")
    
    env_file = __ENV_FILES[env]
    
    load_dotenv(os.path.join(os.getcwd(), env_file))
    
    print(f"ENV = {env}")
