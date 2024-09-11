from abc import ABC, abstractclassmethod
from random import choice




class PlayerTemplate(ABC):
    
    @abstractclassmethod
    def _avaliables_moves(self):
        pass
    
    @abstractclassmethod
    def _make_move(self):
        pass
    
    @abstractclassmethod
    def get_name(self):
        pass

class RandomPlayer(PlayerTemplate):
    def __init__(self):
        self.__name = "Random"

    def _avaliables_moves(self, board):
        """
            Verifies the possible moves available on the board.

            Inputs:
                board: board where the game is played.
            returns: 
                list of available cells to play.
        """
        return [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == '.']

    def _make_move(self, board):
        """
            Selects a random cell out of the ones available to play.
                Inputs:
                    board: board where the game is played.
                returns: 
                    tuple containing the coordinates of the cell where the agent is going to play.
        """
        return choice(self.__disp_moves(board))

    def get_name(self):
        """
            Returns the name of the player.
            return: Name of the player.
        """
        return self.__name