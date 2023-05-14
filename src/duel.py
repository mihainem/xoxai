
import asyncio
import json
#import secrets

import websockets
import game as xox
import constants as c


JOIN_DICT = {}

#WATCH = {}

async def inform(websocket, message):
    """
    Send an informing message to display to the user while playing.

    """
    event = {
        c.EVENT_NAME: c.INFORM,
        c.EVENT_DATA: message,
    }

    print("DUEL Sending error message:", message)
    await websocket.send(json.dumps(event))

async def error(websocket, message):
    """
    Send an error message.

    """
    event = {
        c.EVENT_NAME: c.ERROR,
        c.EVENT_DATA: message,
    }

    print("DUEL Sending error message:", message)
    await websocket.send(json.dumps(event))


async def start(websocket, join_key):
    """
    Handle a connection from the first player: start a new game.

    """
    # FirstCheck if the game already exists
    if join_key in JOIN_DICT:
        await error(websocket, "Game already exists.")
        return
    
    # Initialize a Connect Four game, the set of WebSocket connections
    # receiving moves from this game, and secret access tokens.
    game = xox.Game()
    connected = {websocket}

    #join_key = secrets.token_urlsafe(12)
    JOIN_DICT[join_key] = game, connected

    #watch_key = secrets.token_urlsafe(12)
    #WATCH[watch_key] = game, connected

    try:
        # Send the secret access tokens to the browser of the first player,
        # where they'll be used for building "join" and "watch" links.
        event = {
            c.EVENT_NAME: c.INIT_HOST,
            c.EVENT_DATA: {c.CODE: join_key}
            # "watch": watch_key,
        }
        print("Sending init message:", event)
        await websocket.send(json.dumps(event))
        # Receive and process moves from the first player.
        await play(websocket, game, c.PLAYER1, connected, join_key)
    except Exception as e:
        print("DUEL- Error in start():", e)
        await error(websocket, str(e))
    finally:
        del JOIN_DICT[join_key]
        #del WATCH[watch_key]


async def join(websocket, join_key):
    """
    Handle a connection from the second player: join an existing game.

    """
    # Find the TicTacToe game.
    try:
        game, connected = JOIN_DICT[join_key]
        event = {
            c.EVENT_NAME: c.INIT_JOIN,
            c.EVENT_DATA: {c.CODE: join_key}
            # "watch": watch_key,
        }
        await websocket.send(json.dumps(event))
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # If the game already has two players, send an error message.
    if len(connected) >= 2:
        await error(websocket, "Two players are already connected.")
        return
    
    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Send the first move, in case the first player already played it.
        await replay(websocket, game)

        # Receive and process moves from the second player.
        await play(websocket, game, c.PLAYER2, connected, join_key)
    except Exception as e:
        print("DUEL- Error in join():", e)
        await error(websocket, str(e))
        connected.remove(websocket)


async def replay(websocket, game):
    """
    Send previous moves.

    """
    # Make a copy to avoid an exception if game.moves changes while iteration
    # is in progress. If a move is played while replay is running, moves will
    # be sent out of order but each move will be sent once and eventually the
    # UI will be consistent.
    for row, column in game.moves_history.copy():
        event = {
            c.EVENT_NAME: c.REPLAY,
            c.EVENT_DATA: {c.PLAYER: game.board[row][column], c.COL: column, c.ROW: row}
        }
        await websocket.send(json.dumps(event))


async def play(websocket, game, player, connected, join_key):
    """
    Receive and process moves from a player.

    """
    async for message in websocket:
        print("DUEL- Received message:", message)
        event = json.loads(message)
        if event[c.EVENT_NAME] == c.RESET_BOARD:
            print("DUEL- Broadcasting and Resetting board event")
            try:
                game.reset()
                for conn in connected:
                    await conn.send(json.dumps(event))
                #websockets.broadcast(connected, json.dumps(event))
            except Exception as e:
                print("DUEL- Error resetting board:", e)
                await error(websocket, str(e))
            
            
        elif event[c.EVENT_NAME] == c.LEAVE_ROOM:
            print("DUEL- Leaving room event received")
            await websocket.send(json.dumps(event))
            del JOIN_DICT[join_key]
            break

        elif event[c.EVENT_NAME] == c.DUEL_PLAY:
            # Set what player started the game
            if game.moves_history == []:
                game.turn = player

            # If it isn't player's turn, send an "error" event
            # and cancel the handler.
            if game.turn != player:
                await inform(websocket, "It is your friend's turn.")
                continue
        
            # Parse a "play" event from the UI.
            try:
                column = event[c.EVENT_DATA][c.COL]
                row = event[c.EVENT_DATA][c.ROW]
                # Play the move.
                game.make_move([row, column], player)
            except Exception as e:
                print("DUEL- Error making move:", e)
                await error(websocket, str(e))
                continue
        

            # Send a "play" event to update the UI.
            event = {
                c.EVENT_NAME: c.DUEL_PLAY,
                c.EVENT_DATA: {c.PLAYER: player, c.COL: column, c.ROW: row}
            }
            websockets.broadcast(connected, json.dumps(event))

            game.check_play_ended()
            # If move is winning, send a "win" event.
            if game.winner is not None:
                win_event = {
                    c.EVENT_NAME: c.GAME_ENDED,
                    c.EVENT_DATA: {c.WINNER: "T" if game.winner == "T" else player }
                }
                print("DUEL- Broadcasting win event: " , win_event)
                websockets.broadcast(connected, json.dumps(win_event))

