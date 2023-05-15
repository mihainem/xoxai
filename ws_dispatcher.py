
import json
import websockets
import asyncio

SET_LANGUAGE = "update-language"
CLOSE_WEBSOCKET = "close-websocket"
EVENT_NAME = "event-name"
DISPATCH_EVENT = "dispatch-event"
EVENT_DATA = "event-data"

def event_to_send(event_name):
    return {EVENT_NAME: DISPATCH_EVENT, EVENT_DATA: event_name}

async def handler():
    async with websockets.connect("ws://localhost:5000") as socket:
        event = event_to_send(SET_LANGUAGE)
        await socket.send(json.dumps(event))
        print(await socket.recv())


asyncio.get_event_loop().run_until_complete(handler())