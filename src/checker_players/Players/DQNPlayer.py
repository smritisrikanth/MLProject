import torch
import torch.nn as nn
from checker_players.Players.Player import Player
from checker_players.Checker_Environment.Board import Board
from checker_players.Interpretters.FlatFeaturesInterpretter import FlatFeaturesInterpretter

#from tensorflow import keras
#from tensorflow.keras import layers as kl

import torch
import torch.nn as nn

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
        return self.get_best_move(board)
    
    
    def learn(self, logger_exit, reward, learning_rate = 0.01):
        winner, current_turn_number, board_state_history, _ = logger_exit
        for turn, board in enumerate(board_state_history):
            board = FlatFeaturesInterpretter.interpret(board)
            y_pred = self.model(board)
            loss = reward[turn-1]
            self.model.zero_grad()
            loss.backward()
            
            with torch.no_grad():
                for param in self.model.parameters():
                    param -= learning_rate * param.grad
        
    
    def create_model(self):
        model = torch.nn.Sequential(
            [
                #we can make the input 32, since half of all pieces are empty
                nn.Flatten(input_shape=(8, 8)),
                nn.Linear(32, 16), nn.ReLU(),
                nn.Linear(16,  8), nn.ReLU(),
                nn.Linear( 8,  4), nn.ReLU(),
                nn.Linear( 4,  1)
            ]
        )
        return model
        
        
        