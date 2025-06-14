# grpc controller


import grpc
from concurrent import futures
import time

import nuclear_pb2
import nuclear_pb2_grpc

class PhysicistServicer(nuclear_pb2_grpc.PhysicistServicer):
     def SendFlow(self, request, context):
        print("Received task list:")
        for task in request.tasklist:
            print(f"Task ID: {task.id}, Payload: {task.payload}, Successors: {task.successors}")
        return nuclear_pb2.SendFlowReply(message=f"Task list received successfully.")
     
     def ExecuteTask(self, request, context):
         id = request.id
         taskdict = {task.id:{'payload': task.payload, 'successors': task.successors} for task in request.tasklist}
         print(taskdict)
         return nuclear_pb2.ExecuteTaskReply(message=f"Executed Task {id} {taskdict[id]['payload']}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nuclear_pb2_grpc.add_PhysicistServicer_to_server(PhysicistServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
