from kafka import KafkaConsumer

import os
import json
import logging

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
DB_NAME = os.environ["DB_NAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

logging.info('KAFKA_TOPIC : ', KAFKA_TOPIC)
logging.info('KAFKA_SERVER : ', KAFKA_SERVER)
logging.info('DB_NAME : ', DB_NAME)
logging.info('DB_USERNAME : ', DB_USERNAME)
logging.info('DB_PASSWORD : ', DB_PASSWORD)
logging.info('DB_HOST : ', DB_HOST)
logging.info('DB_PORT : ', DB_PORT)

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER])

def save_to_db(data):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    person_id = int(location["userId"])
    latitude, longitude = float(location["latitude"]), float(location["longitude"])
    sql = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)
    
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

for message in consumer:
    location_data = json.loads(message.value.decode('utf-8'))
    save_to_db(location_data)