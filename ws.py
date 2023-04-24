import asyncio
import websockets
import json
from events import try_handle_event
from board import Board
from json_checker import Checker, Or

expected_schema = {'event-name': str, 'event-data': Or(str, dict, None)}
checker = Checker(expected_schema)

connected = set()
boards = {}


async def handle_message(websocket, message):
    message = checker.validate(json.loads(message))
    
    if message["event-name"] == "dispatch-event":
        for con in connected:
            if con != websocket:
                await con.send(json.dumps(message))
    else:
        board = boards[websocket.id]
        result = try_handle_event(message, board)

        print(f"Result: {str(result)}")
        await websocket.send(json.dumps(result))


async def server(websocket, path):
    if websocket not in connected:
        connected.add(websocket)
        boards[websocket.id] = Board()
    try:
        async for message in websocket:
            print(f"Received on server: {str(message)}")
            await handle_message(websocket, message)
           
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed {e}")
    finally:
        connected.remove(websocket)


start_server = websockets.serve(server, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


