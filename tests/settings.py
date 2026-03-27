import os

from dotenv import load_dotenv

load_dotenv()


def get_host() -> str:
    host = os.getenv("REMOTE_HOST", None)
    if not host:
        raise EnvironmentError("Environment variable 'REMOTE_HOST' must be provided")
    return host


def get_user() -> str:
    host = os.getenv("REMOTE_USER", None)
    if not host:
        raise EnvironmentError("Environment variable 'REMOTE_USER' must be provided")
    return host


def get_private_key_path() -> str:
    host = os.getenv("PRIVATE_KEY_PATH", None)
    if not host:
        raise EnvironmentError("Environment variable 'PRIVATE_KEY_PATH' must be provided")
    return host
