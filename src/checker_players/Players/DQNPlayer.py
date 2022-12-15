import torch
import torch.nn as nn
from checker_players.Players.Player import Player
from checker_players.Checker_Environment.Board import Board
from checker_players.Interpretters.FlatFeaturesInterpretter import FlatFeaturesInterpretter
import numpy as np
import torcheck

class CheckersNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 8*8 is the board size
        self.fc1 = nn.Linear(32, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 32)
        self.fc4 = nn.Linear(32, 16)
        self.fc5 = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(torch.flatten(x)))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        return self.fc5(x)

class DQNPlayer(Player):
    mlpEvaluator = CheckersNet()
    optimizer = torch.optim.SGD(mlpEvaluator.parameters(), lr=1e-3, momentum=0.9)
    
    def __init__(self, player_number):
        self.player_number = player_number

    def board_state_to_tensor(self, board_state):
        if self.player_number == self.P1:
            board_state = board_state
        else:
            board_state = map(lambda row: map(lambda x: -1*x, row),board_state)
        return torch.tensor([board_state], dtype = torch.float32)

        
    def play(self, board):
        best_move = None
        best_evaluation = float("-inf")

        for move in board.get_possible_next_moves():
            new_board = Board(board.spots, P1_turn= board.player_turn)
            new_board.make_move(move)
            curr_evaluation = self.mlpEvaluator(self.board_state_to_tensor(new_board.spots))[0]
            best_move = move if curr_evaluation > best_evaluation else best_move
            best_evaluation = curr_evaluation if curr_evaluation > best_evaluation else best_evaluation

        return best_move

    def learn(self, winner, board_states):
        if winner != self.player_number:
            for i, state in enumerate(board_states):
                state = FlatFeaturesInterpretter.interpret(state)
                self.mlpEvaluator.train()
                self.optimizer.zero_grad()
                self.mlpEvaluator(self.board_state_to_tensor(state))
                loss = torch.tensor([1-i/len(board_states)], requires_grad=True)
                loss.backward()
                self.optimizer.step()
