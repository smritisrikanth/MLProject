from checker_players.Players.Player import Player
from checker_players.Interpretters.DoubleColumnInterpretter import DoubleColumnInterpretter
import random 
class RandomPlayer(Player):

    def play(self, board):
        flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
        id = lambda x: x

        doubleColumn = DoubleColumnInterpretter().interpret(board)
        friendly_piece_locs = doubleColumn[self.player_number]
        all_simple_moves = [board.get_simple_moves(piece_loc) for piece_loc in friendly_piece_locs]
        all_simple_moves = flat_map(id, all_simple_moves)

        all_capture_moves = [board.get_capture_moves(piece_loc) for piece_loc in friendly_piece_locs]
        all_capture_moves = flat_map(id, all_capture_moves)
        
        all_simple_moves.extend(all_capture_moves)
        return random.choice(all_simple_moves)

    # The random player does no learning
    def learn(reward, board):
        pass