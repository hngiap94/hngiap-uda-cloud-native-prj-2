import time
from concurrent import futures
import os
import json
import logging

import grpc
import location_event_pb2
import location_event_pb2_grpc

from kafka import KafkaProducer

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
logging.info('KAFKA_TOPIC : ', KAFKA_TOPIC)
logging.info('KAFKA_SERVER : ', KAFKA_SERVER)

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class LocationEventServicer(location_event_pb2_grpc.LocationEventServiceServicer):
    def Create(self, request, context):

        request_value = {
            "userId": int(request.userId),
            "latitude": int(request.latitude),
            "longitude": int(request.longitude)
        }
        print(request_value)

        location_data = json.dumps(request_value).encode('utf-8')
        producer.send(KAFKA_TOPIC, location_data)
        producer.flush()

        return location_event_pb2.LocationEventMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_event_pb2_grpc.add_LocationEventServiceServicer_to_server(LocationEventServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)