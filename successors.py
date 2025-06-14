import grpc
import nuclear_pb2
import nuclear_pb2_grpc
import sys
import os
import multiprocessing

def executecommand(payload, id):
    command = payload
    args = ["sh","-c",f"echo Start {command};sleep 1;echo Finish {command};python successors.py {id}"]
    # print(f'Executing {args}')
    os.execlp("/bin/sh",*args)

def main():
    my_id = sys.argv[1]
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = nuclear_pb2_grpc.PhysicistStub(channel)

        request = nuclear_pb2.GetFlowRequest()
        response = stub.GetFlow(request)

        taskdict = {task.id:{'payload': task.payload, 'successors': task.successors} for task in response.tasklist} 
        # Create a list of grpc structed Task objects
        subdict = taskdict[my_id]
        successors = subdict['successors']
        
        for id in successors:
            payload = taskdict[id]['payload']
            # print(f"Successor {id=} {payload=}")
            proc = multiprocessing.Process(target=executecommand, args=(payload, id))
            proc.start()


if __name__ == "__main__":
    main()
