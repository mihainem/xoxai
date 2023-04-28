import asyncio
import websockets
import json
import events
import game
from json_checker import Checker, Or

expected_schema = {'event-name': str, 'event-data': Or(str, dict, None)}
checker = Checker(expected_schema)

connected = set()
games = {}


async def handle_message(websocket, message):
    message = checker.validate(json.loads(message))
    
    if message["event-name"] == "dispatch-event":
        for con in connected:
            if con != websocket:
                await con.send(json.dumps(message))
    else:
        game = games[websocket.id]
        result = events.try_handle_event(message, game)

        print(f"Result: {str(result)}")
        await websocket.send(json.dumps(result))


async def server(websocket, path):
    if websocket not in connected:
        connected.add(websocket)
        games[websocket.id] = game.Game()
    try:
        async for message in websocket:
            print(f"Received on server: {str(message)}")
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed {e}")
    finally:
        connected.remove(websocket)


#print("Server listening on port 5000")
#start_server = websockets.serve(server, "", 5000)
#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()

