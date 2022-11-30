class TestRunner:

    def __init__(self, board, player1, player2, logger):
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
