from checker_players.Interpretters.Interpretter import Interpretter

class DoubleColumnInterpretter(Interpretter):
    def interpret(self, board):
        P1_column = [[x,y] for x in range(board.WIDTH) for y in range(board.HEIGHT) if board.get_spot_info([x,y]) == board.P1]
        P2_column = [[x,y] for x in range(board.WIDTH) for y in range(board.HEIGHT) if board.get_spot_info([x,y]) == board.P2]
        return {board.P1: P1_column, board.P2: P2_column}