from api_request import get_weather_data
import psycopg2
import logging
import json
import os
from psycopg2.extensions import cursor as Cursor

logger = logging.getLogger(__name__)

def create_table(cur: Cursor) -> None:
    """Creates the table in the database if it does not already exist."""

    logger.info(f"Creating table if not exists...")
    try:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw__weather_data (
            id SERIAL PRIMARY KEY,
            city TEXT,
            temperature FLOAT,
            weather_descriptions TEXT,
            wind_speed FLOAT,
            time TIMESTAMP,
            inserted_at TIMESTAMP DEFAULT NOW(),
            utc_offset TEXT 
            )""")

        logger.info(f"Table created successfully.")

    except psycopg2.Error as e:
        logger.error(f"Error while trying to create table: {e.__class__.__name__}: {e}")
        raise

def insert_records(data: dict, cur: Cursor) -> None:
    """Inserts the data provided in the 'data' dictionary into the database using the provided cursor."""

    logger.info(f"Inserting weather records into the database...")
    location = data.get('location')
    weather = data.get('current')
    if not location or not weather:
        logger.error(f"Data received from the API is incomplete, misses a key information located in data['location'] or data['weather']")
        raise KeyError(location)

    try:
        cur.execute("""
            INSERT INTO dev.raw__weather_data (city, temperature, weather_descriptions, wind_speed, time, inserted_at, utc_offset)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)""", 
            (location['name'], weather['temperature'], weather['weather_descriptions'][0], weather['wind_speed'],
            location['localtime'], location['utc_offset']
            ))

        logger.info("Data inserted successfully")
        
    except psycopg2.Error as e:
        logger.error(f"Error while trying to insert records: {e.__class__.__name__}: {e}")
        raise


def uploader() -> None:
    """Orchestrator of the data upload process. It fetches the weather data and uploads it to the database."""

    logger.info(f"Starting to upload data to the database...")
    data = get_weather_data()
    try:
        with psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'db'),
            dbname=os.getenv('POSTGRES_DB', 'db'),
            user=os.getenv('POSTGRES_USER', 'db_user'),
            password=os.environ['POSTGRES_ROOT_PASSWORD'],
            port=int(os.getenv('POSTGRES_PORT', '5432')),
        ) as conn:
            with conn.cursor() as cur:
                create_table(cur)
                insert_records(data, cur)
        print("Data uploaded successfully.")
    except psycopg2.Error as e:
        logger.error(f"An error occurred while trying to connect to the database: {e.__class__.__name__}: {e}")
        raise
