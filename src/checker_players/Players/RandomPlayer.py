from checker_players.Players.Player import Player
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
import random 
class RandomPlayer(Player):

    def play(self, board):
        doubleColumn = DoubleColumnInterpretter.interpret(board)
        friendly_piece_locs = doubleColumn[self.player_number]
        random_piece_loc = random.choice(friendly_piece_locs)
        simple_moves = board.get_simple_moves(random_piece_loc)
        capture_moves = board.get_capture_moves(random_piece_loc)
        simple_moves.extend(capture_moves)

        random_move = random.choise(simple_moves)
        board.make_move(random_move)

    # The random player does no learning
    def learn(reward, board):
        pass