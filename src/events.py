import ai
import json
import localizations
ai = ai.AI()
events = {}

def set_player_move(game, data):
    row,col = move = [int(data["row"]), int(data["col"])]
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    game.make_move(move, player_symbol)
    result = game.check_play_ended()
    return result or "Server set move to: " + str(move) + " index: " + str(col + row*3)

def get_ai_hint(game, data):
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    player_think_time = data.get("player-think-time", -1)
    if game.is_board_full():
        game.reset()
        return "Invalid board state"
    else:
        row,col = ai.get_ai_move(game, player_think_time)
        return {"row":row, "col":col}

def get_hint(game, data):
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    enemy_symbol = player_symbol == 'X' and 'O' or 'X'
    if game.is_board_full():
        game.reset()
        return "Invalid board state"
    else:
        row,col = game.next_best_move(player_symbol, enemy_symbol)
        return {"row":row, "col":col}
    
def undo_move(game, data):
    no_of_undos = int(data["no-of-undos"])
    for i in range(no_of_undos):
        game.undo_move()
    return f"Undid {no_of_undos} moves"

def reset_board(game):
    game.reset()
    ai.reset_ai()
    return "board is now reset"

def dispatch_event(data):
    return data


events["set-move"] = lambda game,data: set_player_move(game, data)
events["get-ai-hint"] = lambda game,data: get_ai_hint(game, data)
events["get-hint"] = lambda game,data: get_hint(game, data)
events["undo-move"] = lambda game,data: undo_move(game, data)
events["reset-board"] = lambda game, data: reset_board(game)
events["get-language"] = lambda game, data: localizations.get_language_dict(data)
events["dispatch-event"] = lambda game, data: dispatch_event(data)

def try_handle_event(message, game):
    name = message["event-name"]
    content = message["event-data"]
    message["event-data"] = events.get(name, lambda game,data: "Invalid event")(game, content)
    return message