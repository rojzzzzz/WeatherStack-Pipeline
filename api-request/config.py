import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def load_env(key: str) -> str:
    """Loads the environment variables from the .env file"""
    try:
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"Environment variable '{key}' not found.")
        return value
    except KeyError:
        logger.error(f"Failed to load environment variable: {key}")
        raise

API_KEY = load_env("API_KEY")
ENDPOINT = load_env("ENDPOINT")
logger.info("Environment variables loaded successfully")