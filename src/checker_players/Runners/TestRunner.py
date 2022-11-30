class TestRunner:

    def __init__(self, type_of_game, player1, player2, logger):
        self.type_of_game = type_of_game
        self.player1 = player1
        self.player2 = player2
        self.logger = logger

    def play_single_game(self, turn_cutoff = 1000):
        board = self.type_of_game()
        self.logger.begin()
        for i in range(turn_cutoff):
            self.logger.apply(board, self.player1, self.player2)
            if board.is_game_over():
                break
            curr_player = self.player1 if (board.player_turn == board.P1_turn) else self.player2
            board.make_move(curr_player.play(board))
        self.logger.end()
        return self.logger.exit()
