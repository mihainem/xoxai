
import json
import websockets
import asyncio
import constants as c

SET_LANGUAGE = "update-language"
CLOSE_WEBSOCKET = "close-websocket"


def event_to_send(event_name):
    return {c.EVENT_NAME: c.DISPATCH_EVENT, c.EVENT_DATA: event_name}

async def handler():
    #websocket = next(iter(connected))
    async with websockets.connect("ws://localhost:5000") as socket:
        event = event_to_send(SET_LANGUAGE)
        await socket.send(json.dumps(event))
        print(await socket.recv())


asyncio.get_event_loop().run_until_complete(handler())