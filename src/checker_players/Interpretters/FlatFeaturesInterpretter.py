from checker_players.Interpretters.Interpretter import Interpretter

class FlatFeaturesInterpretter(Interpretter):
    def interpret(self, board):
        features = list()
        for x in range(board.WIDTH):
            for y in range(board.HEIGHT):
                if (x+y) % 2 == 1:
                    features.append(board.spots[x][y])
        return features