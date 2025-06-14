# babyencrico
execute a flow of concurrent and sequential tasks using grpc and operating system processes

## Setup

### Virtual environment

Do the usual .venv setup with requirements.txt

### Build prototype stubs


Use protoc to generate the _pb2.py and _pb2_grpc.py files

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. nuclear.proto
```

## Usage

Pass a job flow like

```
[
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
        "payload": "Requirement analysis",
        "successors": ["D"]
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
```
## Start the server

Just run the controller

```
python controller.py
```

## Now make a client connect to it and send it a list of jobs

Via the cleverly named client.py

```
python client.py
```

Note that the client returns immediately, but the jobs are running both sequentially and concurrently on the server

