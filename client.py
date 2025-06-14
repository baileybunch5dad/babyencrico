import grpc
import nuclear_pb2
import nuclear_pb2_grpc

def main():
    tasks = [
        {
            "id": "A",
            "payload": "Start project",
            "successors": ["B", "C"]
        },
        {
            "id": "B",
            "payload": "Design phase",
            "successors": ["D"]
        },
        {
            "id": "C",
            "payload": "Documentation",
            "successors": []
        },
        {
            "id": "D",
            "payload": "Implementation",
            "successors": ["E"]
        },
        {
            "id": "E",
            "payload": "Testing",
            "successors": ["F"]
        },
        {
            "id": "F",
            "payload": "Deployment",
            "successors": []
        }
    ]

    for t in tasks:
        print(t)

    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = nuclear_pb2_grpc.PhysicistStub(channel)

        # Create a list of grpc structed Task objects
        grpctasklist=[nuclear_pb2.Task(id=t['id'], payload=t['payload'], successors=t['successors']) for t in tasks]

        # Create and send the request
        request = nuclear_pb2.SendFlowRequest(tasklist=grpctasklist)
        response = stub.SendFlow(request)
        print("Server response:", response.message)

        request = nuclear_pb2.ExecuteTaskRequest(id='A')
        response = stub.ExecuteTask(request)
        print("Server response:", response.message)



if __name__ == "__main__":
    main()