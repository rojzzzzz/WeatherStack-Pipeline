from config import API_KEY, ENDPOINT
import requests
import logging

logger = logging.getLogger(__name__)

def get_weather_data() -> dict:
    """Requests the current weather data for New York from the API and returns the JSON response."""

    logger.info("Starting API request...")
    params = {'access_key': API_KEY, 'query': 'New York'}
    url = f"{ENDPOINT}/current"

    try:
        response = requests.get(url, params=params, timeout=(3, 20))
        response.raise_for_status()
        logger.info("API request successful.")
        return response.json()
    
    except requests.exceptions.ConnectTimeout as e:
        logger.error(f"Failed to connect in time. {e.__class__.__name__}: {e}")
        raise
    except requests.exceptions.ReadTimeout as e:
        logger.error(f"Server didn't send data in time. {e.__class__.__name__}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while trying to request data from the API: {e.__class__.__name__}: {e}")
        raise
    

