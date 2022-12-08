import grpc
import location_event_pb2
import location_event_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_event_pb2_grpc.LocationEventServiceStub(channel)

# Update this with desired payload
item1 = location_event_pb2.LocationEventMessage(
    userId=1,
    coordinateX=100,
    coordinateY=200
)
item2 = location_event_pb2.LocationEventMessage(
    userId=2,
    coordinateX=-100,
    coordinateY=-200
)



response = stub.Create(item1)
response = stub.Create(item2)