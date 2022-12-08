import numpy as np

class TrainRunner:

    def __init__(self, board, player1, p1model, player2, p2model, logger):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.logger = logger

    def play_single_game(self, turn_cutoff = 1000):
        self.logger.begin()
        for _ in range(turn_cutoff):
            if self.board.is_game_over():
                break
            curr_player = self.player1 if self.board.player_turn else self.player2
            self.board.make_move(curr_player.play(self.board))
            self.logger.apply(self.board, self.player1, self.player2)
        self.logger.end()
        return self.logger.exit()
    
    def train_single_game(self, turn_cutoff=1000): #maybe add more parameters
        logger_exit = self.play_single_game(turn_cutoff)
        p1reward = self.calc_reward(logger_exit)
        self.player1.learn(logger_exit, p1reward)
        self.player2.learn(logger_exit, -p1reward)
        return
        
    def calc_reward(logger_exit):
        p1final_reward = 10 if logger_exit[0] == 1 else -10
        p1reward = np.linspace(0, p1final_reward/(logger_exit[1]**0.5), num=logger_exit[1])
        return p1reward