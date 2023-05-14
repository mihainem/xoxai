import ai
import json
import localizations
from game import Game
import duel
import asyncio
import constants as c

ai = ai.AI()
events = {}

def set_player_move(game, data):
    row,col = move = [int(data[c.ROW]), int(data[c.COL])]
    player_symbol = data[c.IS_FIRST_PLAYER] and 'X' or 'O'
    game.make_move(move, player_symbol)
    result = game.check_play_ended()
    return result or "Server set move to: " + str(move) + " index: " + str(col + row*3)

def get_ai_hint(game, data):
    player_symbol = data[c.IS_FIRST_PLAYER] and 'X' or 'O'
    player_think_time = data.get(c.PLAYER_THINK_TIME, -1)
    if game.is_board_full():
        game.reset()
        return "Invalid board state"
    else:
        row,col = ai.get_ai_move(game, player_think_time)
        return {c.ROW:row, c.COL:col}

def get_hint(game, data):
    player_symbol = data[c.IS_FIRST_PLAYER] and 'X' or 'O'
    enemy_symbol = player_symbol == 'X' and 'O' or 'X'
    if game.is_board_full():
        game.reset()
        return "Invalid board state"
    else:
        row,col = game.next_best_move(player_symbol, enemy_symbol)
        return {c.ROW:row, c.COL:col}
    
def undo_move(game, data):
    no_of_undos = int(data[c.NO_OF_UNDOS])
    for i in range(no_of_undos):
        game.undo_move()
    return f"Undid {no_of_undos} moves"

def reset_board(game):
    game.reset()
    ai.reset_ai()
    return "board is now reset"

def dispatch_event(data):
    return data

async def init_new_host(websocket, data):
    code = data[c.EVENT_DATA][c.CODE]
    await duel.start(websocket, code)

async def init_new_join(websocket, data):
    code = data[c.EVENT_DATA][c.CODE]
    await duel.join(websocket, code)

def duel_play(websocket, data):
    print(data)
    
    

events[c.SET_MOVE] = lambda game,data: set_player_move(game, data)
events[c.GET_AI_HINT] = lambda game,data: get_ai_hint(game, data)
events[c.GET_HINT] = lambda game,data: get_hint(game, data)
events[c.UNDO_MOVE] = lambda game,data: undo_move(game, data)
events[c.RESET_BOARD] = lambda game, data: reset_board(game)
events[c.GET_LANGUAGE] = lambda game, data: localizations.get_language_dict(data)
events[c.DISPATCH_EVENT] = lambda game, data: dispatch_event(data)
events[c.INIT_HOST] = lambda websocket, data: init_new_host(websocket, data)
events[c.INIT_JOIN] = lambda websocket, data: init_new_join(websocket, data)
events[c.DUEL_PLAY] = lambda websocket, data: duel_play(websocket, data)


games = {}

def try_handle_event(message, websocket):
    name = message["event-name"]
    content = message["event-data"]
    
    game = games.get(websocket.id, Game())
    games[websocket.id] = game
    message["event-data"] = events.get(name, lambda game,data: "Invalid event")(game, content)
    return message