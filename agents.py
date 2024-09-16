from utils import Board, heuristic
from abc import ABC, abstractclassmethod
from random import choice
import time
from typing import Tuple
import os
import numpy as np
import copy





# TODO: Check and fix type checks.
class PlayerTemplate(ABC):
    
    @classmethod
    def _available_moves(cls, board: Board) -> list:
        """
            Verifies the possible moves available on the board.

            Inputs:
                board: board where the game is played.
            returns: 
                list of available cells to play.
        """
        return [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == ' ']
    
    @abstractclassmethod
    def make_move(self) -> None:
        pass
    
    @abstractclassmethod
    def get_name(self) -> None:
        pass
    
    @abstractclassmethod
    def get_piece(self) -> None:
        pass

class RandomPlayer(PlayerTemplate):
    def __init__(self, piece):
        self.__name = "Random"
        self.__piece = piece

    def make_move(self, board: Board) -> Tuple[int, int]:
        """
            Selects a random cell out of the ones available to play.
                Inputs:
                    board: board where the game is played.
                returns: 
                    tuple containing the coordinates of the cell where the agent is going to play.
        """
        raw_board = board.get_board()
        return choice(PlayerTemplate._available_moves(raw_board))

    def get_name(self) -> str:
        """
            Returns the name of the player.
            return: Name of the player.
        """
        return self.__name
    
    def get_piece(self) -> str:
        return self.__piece

class GreedyPlayer(PlayerTemplate):
    def __init__(self, piece) -> None:
        self.__name = "Greedy"
        self.__piece = piece
    
    def make_move(self, board: Board) -> Tuple[int, int]:
        """
            Chooses the move to make based in a greedy approach.

            Inputs:
                board(Board): current game board.
            Returns:
                (tuple) coordinates to place the piece. 
        """
        moves_rank = []
        raw_board = copy.deepcopy(board.get_board())
        av_moves = PlayerTemplate._available_moves(raw_board)
        score = 0

        for move in av_moves:
            score += heuristic(move, raw_board, self.__piece) # Check places where it can have two pieces in a row. 
            score += heuristic(move, raw_board, self.__piece, piece_count=3, val=100) # Checks if the position is a winning position.
            # Checks if the position is a winning position for the rival.
            score += heuristic(move, raw_board, self.__piece, piece_count=2, val=25, only_block=True) 
            # Adds the move to the rank.
            moves_rank.append((score, move))
        
        # Sorting the rank
        moves_rank = sorted(moves_rank, key=lambda x: x[0], reverse=True)
        
        return moves_rank[0][1] 
            
    def get_name(self) -> str:
        """
            Returns the players' name.
        """
        return self.__name
    
    def get_piece(self) -> str:
        """
            Returns the player's piece.
        """
        return self.__piece
    

class GameManager:
    @staticmethod
    def select_players() -> list:
        """
            Selects the players that will be playing the game.

            returns:
                List of classes, corresponding to the players.
        """
        players = {
            '1' : RandomPlayer,
            '2' : GreedyPlayer
        }
        selected_players = []

        # Repeating until it has enough players.
        while len(selected_players) < 2:
            print("\n1. Random\n2. Greedy\n3. MinMax\n")
            input_ = input(f"Select the {len(selected_players) + 1} player: ")

            player = players.get(input_, None)

            # Adding the selected player.
            if player != None:
                selected_players.append(player('X' if len(selected_players) <= 0 else 'O'))

        return selected_players

    def start(self) -> None:
        """
            Simulates a game between two players, alternating between them until one wins or the game ends in a tie. 
        """
        # Obtaining the players to play with.
        players = self.select_players()

        assert len(players) == 2 , "Number of players needs to be two."

        board = Board()
        game_ended = False

        # Initializing the game.
        while not game_ended:
            for player in players:
                piece = player.get_piece()
                # Making and placing the move.
                move = player.make_move(board)

                board.place_piece(move, piece)

                # Cleaning the screen
                os.system('cls')

                # Printing the board
                print(f"Player {piece} turn.")
                print(board)

                time.sleep(1)

                # Checking if the game was won by the player
                if board.player_won(piece):
                    print(f'{player.get_name()} won!')
                    game_ended = True
                    break
                
                # Checking if the game is a tie
                elif board.tie():
                    print("Game is a tie!")
                    game_ended = True
                    break