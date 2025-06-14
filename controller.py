# grpc controller


import grpc
from concurrent import futures
import time
import subprocess
import multiprocessing
import os
import nuclear_pb2
import nuclear_pb2_grpc

class PhysicistServicer(nuclear_pb2_grpc.PhysicistServicer):
     def SendFlow(self, request, context):
        print("Received task list:")
        self.taskdict = {task.id:{'payload': task.payload, 'successors': task.successors} for task in request.tasklist}
        for task in request.tasklist:
            print(f"Task ID: {task.id}, Payload: {task.payload}, Successors: {task.successors}")
        return nuclear_pb2.SendFlowReply(message=f"Task list received successfully.")
     
     def GetFlow(self, request, context):
        grpctasklist=[nuclear_pb2.Task(id=key, payload=val['payload'], successors=val['successors']) for key,val in self.taskdict.items()]
        return nuclear_pb2.GetFlowReply(tasklist=grpctasklist)
     
     def ExecuteTask(self, request, context):
         id = request.id
         payload = self.taskdict[id]['payload']
         #  print(f"{id=} {payload=}")
         proc = multiprocessing.Process(target=executecommand, args=(payload, id))
         proc.start()
         #  result = subprocess.run(oscommand, shell=True, capture_output=True, text=True)
         message = f"{id=} launched {payload}"
         return nuclear_pb2.ExecuteTaskReply(message=message)

def executecommand(payload, id):
    command = payload
    args = ["sh","-c",f"echo Start {command};sleep 1;echo Finish {command};python successors.py {id}"]
    # print(f'Executing {args}')
    os.execlp("/bin/sh",*args)

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
