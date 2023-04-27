import random
from board import Game

class AI:
    def __init__(self):
        self.ai_agility_time = 1 # second
        self.ai_smartness = 80 # 80 % smartness
        self.rand_num = 100 
        
    def reset_ai(self):
        self.rand_num = random.randint(1,100)

    def ai_should_play_smart(self, wins=0, losses=0, player_think_time = 0):
        if player_think_time <= 0:
            player_think_time = self.ai_agility_time
            
        player_think_time = min(player_think_time, self.ai_agility_time)

        #make sure the division by total will not result in DivisionByZeroException
        total = max(wins + losses, 1)

        #ai should take in consideration wins and loses after a minimum of 5 plays
        if total < 5:
            wins = losses = 0
        
        #from the current smartness fa
        multiplier = self.ai_smartness / 2

        ai_score = self.ai_smartness - (self.ai_agility_time - player_think_time ) * (multiplier / self.ai_agility_time) + (wins - losses) * (multiplier / total)
        
        print(f"Computer's score would be: {ai_score} knowing we have {wins} wins and {losses} losses, while random number is: {self.rand_num}")
        return self.rand_num <= ai_score
    

    def get_ai_move(self, board, player_time=-1):
        print(f"history: {board.history}")
        print("received player time: ",player_time)
        player = 'X'
        enemy = 'O'
        wins = board.history.count(player)
        losses = board.history.count(enemy)
        if self.ai_should_play_smart(wins, losses, player_time):
            print("Computer is playing smart!")
            return board.next_best_move(enemy, player)
        return board.wrong_move(enemy)

