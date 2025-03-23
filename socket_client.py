import websocket
import json
import os
from dotenv import load_dotenv

load_dotenv()

ws = websocket.WebSocket()
ws.connect(os.getenv("SOCKET_URL"))

request = {
    "type": "ModifyQuerySet",
    "baseVersion": 0,
    "newVersion": 1,
    "modifications": [
        {
            "type": "Add",
            "queryId": 0,
            "udfPath": "events:get",
            "args": [{}]
        }
    ]
}

request_by_eventId = {
    "type": "ModifyQuerySet",
    "baseVersion": 0,
    "newVersion": 1,
    "modifications": [
        {
            "type": "Add",
            "queryId": 0,
            "udfPath": "events:getById",
            "args": [
                {
                    "eventId": "jh7caz2et0e2chzhcyq5q94vts7byke8"
                }
            ]
        },
        {
            "type": "Add",
            "queryId": 1,
            "udfPath": "events:getEventAvailability",
            "args": [
                {
                    "eventId": "jh7caz2et0e2chzhcyq5q94vts7byke8"
                }
            ]
        }
    ]
}

# Sending JSON request
ws.send(json.dumps(request))
response = json.loads(ws.recv())
events = response["modifications"][0]["value"]

# ws.send(json.dumps(request_by_eventId))

ws.close()