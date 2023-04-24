import random
from board import Board

class AI:
    def __init__(self):
        self.smartnessTime = 5
        self.smartnessFactor = 80
        

    def ai_should_play_smart(self, wins=0, losses=0, player_time = -1):
        if player_time == -1:
            player_time = self.smartnessTime

        total = max(wins + losses, 1)
        multiplier = self.smartnessFactor / 2

        ai_score = self.smartnessFactor - (self.smartnessTime - player_time ) * (multiplier / self.smartnessTime) + (wins - losses) * (multiplier / total)
        rand_num = random.randint(1,100)
        print(f"Computer's score would be: {ai_score} knowing we have {wins} wins and {losses} losses, while random number is: {rand_num}")
        return rand_num <= ai_score
    

    def get_ai_move(self, board):
        print(f"history: {board.history}")
        player = 'X'
        enemy = 'O'
        wins = board.history.count(player)
        losses = board.history.count(enemy) + board.history.count('T')
        if self.ai_should_play_smart(wins, losses):
            print("Computer is playing smart!")
            return board.next_best_move(enemy, player)
        return board.wrong_move(enemy)

