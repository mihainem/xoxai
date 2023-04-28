
import json
import websockets
import asyncio

SET_LANGUAGE = "update-language"
CLOSE_WEBSOCKET = "close-websocket"


def event_to_send(event_name):
    return {"event-name": "dispatch-event","event-data": event_name}

async def handler():
    #websocket = next(iter(connected))
    async with websockets.connect("ws://localhost:5000") as socket:
        event = event_to_send(SET_LANGUAGE)
        await socket.send(json.dumps(event))
        print(await socket.recv())


asyncio.get_event_loop().run_until_complete(handler())



# make flag icons for each of the following codes: en, ro, fr, de, ja
