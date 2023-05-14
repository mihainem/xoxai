import asyncio
import websockets
import json
import events
import game
import constants as c
from json_checker import Checker, Or

expected_schema = {'event-name': str, 'event-data': Or(str, dict, None)}
checker = Checker(expected_schema)

connected = set()
games = {}


async def handle_message(websocket, message):
    message = checker.validate(json.loads(message))
    
    if message[c.EVENT_NAME] == c.DISPATCH_EVENT:
        message[c.EVENT_NAME] = message[c.EVENT_DATA]
        for con in connected:
            if con != websocket:
                await con.send(json.dumps(message))
    else:
        name = message[c.EVENT_NAME]
        if message[c.EVENT_NAME] in [c.INIT_HOST, c.INIT_JOIN]:
            await events.events[name](websocket, message )   
        else: 
            result = events.try_handle_event(message, websocket)

            if result is not None:
                print(f"Result: {str(result)}")
                await websocket.send(json.dumps(result))


async def server(websocket, path):
    if websocket not in connected:
        connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received on server: {str(message)}")
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed {e}")
    finally:
        connected.remove(websocket)
