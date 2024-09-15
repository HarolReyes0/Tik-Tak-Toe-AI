import numpy as np
from typing import Tuple
import copy


class Board:
    """
    This class creates the game board, this board consist in a 3 x 3 matrix
    full of zeros.
    """
    def __init__(self):
        self.__board = np.full((3, 3), ' ')
    
    def __str__(self):
        """
            Prints the board in a more readable format.
        """
        board = ""

        for i, row in enumerate(self.__board):
            for j, cell in enumerate(row):
                board += cell  # Add the current cell to the board
                if j < len(row) - 1:  # Add '|' between the cells, but not after the last one
                    board += ' | '
            board += '\n'  # New line after each row
            if i < len(self.__board) - 1:  # Add horizontal separator after each row, except the last one
                board += '- + - + -\n'
            
        return board

    def place_piece(self, coordinates: Tuple[int, int], piece: str):
        """
        Adds the player's piece on the cell selected.

        Inputs:
                coordinates: coordinates where the piece is going to be placed.
                piece: symbol to be placed.
        """
        self.__board[coordinates] = piece

    def player_won(self, piece: str) -> bool:
        """
        Verifies if the game has been won by the player by checking if there is tree consecutive marks from the same
        plater in any of the row, columns or diagonals.

        :param player: Player's piece.

        :return: Boolean indicating if the game has been won by the player.
        """

        # Checks diagonals
        main_diagonal = lambda board, piece: all([piece == board[i, i] for i in range(board.shape[0])])
        secondary_diagonal = lambda board, piece: all([piece == board[i, 2 - i] for i in range(board.shape[0])])
        # Checks if any of the column is full of the player's piece
        columns = lambda board, piece: any([True if all(row == piece) else False for row in board.T])
        # Checks any of the rows is full of the player's piece
        rows = lambda board, piece: any([True if all(row == piece) else False for row in board])

        # Verifying if the player won.
        if any([main_diagonal(self.__board, piece), secondary_diagonal(self.__board, piece),
                columns(self.__board, piece), rows(self.__board, piece),]):
            return True
        else:
            return False


    def tie(self) -> bool:
        """
        Verifies if the game is a tie (none of the player won and there is no other move that can be made).

        :return: Boolean indicating if the game is tied.
        """
        return all((self.__board != ' ').flatten())
    
    def get_board(self):
        return self.__board


def heuristic(coordinates: Tuple[int, int], board: Board, piece: str, val= 5, piece_count= 2) -> int:
    """
        Calculates the heuristic value of a given choice based on the amount of consecutive pieces placed.

        Inputs:
                coordinates(tuple): Coordinates to place the piece.
                board(Boar): Current GameBoard.
                piece(Piece): piece to place in the board.
                val(int): Heuristic value in case that the conditions are fulfilled.
                piece_count(int): amount of pieces to check if placed consecutive.
        Outputs:
                int: heuristic score normalized
    """
    score = 0
    rival_piece = 'X' if piece == 'O' else 'O'

    # Create a copy of the board and place the piece
    board_copy = copy.deepcopy(board)
    board_copy.place_piece(coordinates, piece)
    matrix_board = board_copy.get_board()

    row, col = coordinates

    # Define the evaluation function
    def evaluate_line(block = False):
        def moving_to_win(line):
            if (line == piece).sum() == piece_count and (line == rival_piece).sum() == 0:
                return val
            else:
                return 0
            
        def moving_to_block(line):
            if (line == rival_piece).sum() == 2 and (line == piece).sum() == 1:
                return val
            else:
                return 0
        
        if block:
            return moving_to_block
        
        return moving_to_win

    # Evaluate the row
    row_line = matrix_board[row, :]
    score += evaluate_line(row_line)

    # Evaluate the column
    col_line = matrix_board[:, col]
    score += evaluate_line(col_line)

    # Evaluate the main diagonal if applicable
    if row == col:
        main_diag = np.diag(matrix_board)
        score += evaluate_line(main_diag)
    
    # Evaluate the anti-diagonal if applicable
    if row + col == 2:
        anti_diag = np.diag(np.fliplr(matrix_board))
        score += evaluate_line(anti_diag)

    return score / (val * 3)