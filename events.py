from ai import AI
import json
from localizations import get_language_dict

ai = AI()
events = {}

def set_player_move(board, data):
    row,col = move = [int(data["row"]), int(data["col"])]
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    board.make_move(move, player_symbol)
    result = board.check_play_ended()
    return result or "Server set move to: " + str(move) + " index: " + str(col + row*3)

def get_ai_hint(board, data):
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    enemy_symbol = player_symbol == 'X' and 'O' or 'X'
    if board.is_board_full():
        board.reset()
        return "Invalid board state"
    else:
        row,col = ai.get_ai_move(board)
        return {"row":row, "col":col}

def get_hint(board, data):
    player_symbol = data["isFirstPlayer"] and 'X' or 'O'
    enemy_symbol = player_symbol == 'X' and 'O' or 'X'
    if board.is_board_full():
        board.reset()
        return "Invalid board state"
    else:
        row,col = board.next_best_move(player_symbol, enemy_symbol)
        return {"row":row, "col":col}
    
def undo_move(board, data):
    no_of_undos = int(data["no-of-undos"])
    for i in range(no_of_undos):
        board.undo_move()
    return f"Undid {no_of_undos} moves"

def reset_board(board):
    board.reset()
    return "board is now reset"

def dispatch_event(data):
    return data


events["set-move"] = lambda board,data: set_player_move(board, data)
events["get-ai-hint"] = lambda board,data: get_ai_hint(board, data)
events["get-hint"] = lambda board,data: get_hint(board, data)
events["undo-move"] = lambda board,data: undo_move(board, data)
events["reset-board"] = lambda board, data: reset_board(board)
events["get-language"] = lambda board, data: get_language_dict(data["language-code"])
events["dispatch-event"] = lambda board, data: dispatch_event(data)

def try_handle_event(message, board):
    name = message["event-name"]
    data = message["event-data"]
    message["event-data"] = events.get(name, lambda board,data: "Invalid event")(board, data)
    return message