from utils import Board, calculate_heuristic
from abc import ABC, abstractclassmethod
from random import choice
import time
from typing import Tuple
import os
import numpy as np
import copy

# TODO: Fix bug; not showing human player name after winning. 




class PlayerTemplate(ABC):
    
    @classmethod
    def _available_moves(cls, board: np.array) -> list:
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
        queue = []
        raw_board = copy.deepcopy(board.get_board())
        av_moves = PlayerTemplate._available_moves(raw_board)

        for move in av_moves:
            # Calculating the heuristic score.
            score = calculate_heuristic(move, raw_board, self.__piece)
            # Adds the state to the queue.
            queue.append((score, move))
        
        # Sorting the rank
        queue = sorted(queue, key=lambda x: x[0], reverse=True)
        
        return queue[0][1] 
            
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
    
class HumanPlayer(PlayerTemplate):
    def __init__(self, piece) -> None:
        self.__name = 'Human'
        self.__piece = piece

    def make_move(self, board) -> Tuple[int, int]:
        copied_board = copy.deepcopy(board)
        raw_board = copied_board.get_board()
        av_moves = PlayerTemplate._available_moves(raw_board)
        invalid_input = True
        moves = {}

        # Adding all the available moves on the board.
        for i, move in enumerate(av_moves):
            moves[i] = move
            copied_board.place_piece(move, i)
        
        print(copied_board)

        # Obtaining the user's move
        while invalid_input:
            try:
                input_ = int(input("Select your move..."))
            except:
                print('Enter a valid input...')
                continue
            
            move = moves.get(input_, None)

            if move != None:
                break
        
        return move

    def get_name(self) -> str:
        return self.__name
    
    def get_piece(self) -> str:
        return self.__piece

class MinMax(PlayerTemplate):
    def __init__(self, piece) -> None:
        self.__piece = piece
        self.__name = 'MinMax'

    def _maximize(self, board: Board, alpha: int, beta: int, rival_piece: str):
        
        # Verifying if player won.
        if board.player_won(self.__piece):
            return None, 9999
        # Verifying if rival won.
        elif board.player_won(rival_piece):
            return None, -9999
        # Verifying if game was a tie.
        elif board.tie():
            return 0
        
        max_child, max_utility = None, - np.inf

        # Creating a chields.
        for child in PlayerTemplate._available_moves(board):
            # Debugging
            print(child)
            new_board = copy.deepcopy(board)
            new_board.place_piece(child, self.__piece)

            _, utility = self._minimize(new_board, alpha, beta, rival_piece)
            
            # Updating to max values.
            if utility > max_utility:
                max_child, max_utility = child, utility

            # Prunes branch.
            if max_utility >= beta:
                break
            
            # Updating alpha.
            alpha = max(alpha, max_utility)
        
        return max_child, max_utility


    def _minimize(self, board: Board, alpha: int, beta: int, rival_piece: str):
        
        # Verifying if player won.
        if board.player_won(self.__piece):
            return None, 9999
        # Verifying if rival won.
        elif board.player_won(rival_piece):
            return None, -9999
        # Verifying if game was a tie.
        elif board.tie():
            return 0
        
        min_child, min_utility = None, np.inf

        # Creating a chields.
        for child in PlayerTemplate._available_moves(board):
            new_board = copy.deepcopy(board)
            new_board.place_piece(child, self.__piece)

            _, utility = self._maximize(new_board, alpha, beta, rival_piece)
            
            # Updating to max values.
            if utility < min_utility:
                min_child, min_utility = child, utility

            # Prunes branch.
            if min_utility <= alpha:
                break
            
            # Updating alpha.
            alpha = min(alpha, min_utility)
        
        return min_child, min_utility

    def make_move(self, board: Board) -> Tuple[int, int]:
        # Selecting rival piece.
        rival_piece = 'X' if self.__piece == 'O' else 'O'

        child, _ = self._maximize(board, - np.inf, np.inf, rival_piece)

        return child
    
    def get_name(self) -> None:
        return self.__name
    
    def get_piece(self) -> None:
        self.__piece


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
            '2' : GreedyPlayer,
            '3' : HumanPlayer,
            '4' : MinMax
        }
        selected_players = []

        # Repeating until it has enough players.
        while len(selected_players) < 2:
            print("\n1. Random\n2. Greedy\n3. Human\n4. MinMax")
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