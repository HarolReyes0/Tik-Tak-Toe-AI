import numpy as np




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

    def place_piece(self, coordinates, symbol):
        """
        Adds the player's piece on the cell selected.

        Inputs:
                coordinates: coordinates where the piece is going to be placed.
                piece: symbol to be placed.
        """
        self.__board[coordinates] = symbol

    def get_board(self):
        return self.__board

def player_won(marker, board) -> bool:
    """
    Verifies if the game has been won by the player by checking if there is tree consecutive marks from the same
    plater in any of the row, columns or diagonals.

    :param player: Mark of the player in the board.
    :param board: Game board.

    :return: Boolean indicating if the game has been won by the player.
    """

    # Checks diagonals
    main_diagonal = lambda board, marker: all([marker == board[i, i] for i in range(board.shape[0])])
    secondary_diagonal = lambda board, marker: all([marker == board[i, 2 - i] for i in range(board.shape[0])])
    # Checks if any of the column is full of the palyer's marker columns
    columns = lambda board, marker: any([True if all(row == marker) else False for row in board.T])
    # Checks any of the rows is full of the palyer's marker
    rows = lambda board, marker: any([True if all(row == marker) else False for row in board])

    # Verifying if any of the conditions are fulfilled.

    if any([main_diagonal(board, marker), secondary_diagonal(board, marker),
            columns(board, marker), rows(board, marker),]):
        return True
    else:
        return False


def tie(board):
    """
    Verifies if the game is a tie (none of the player won and there is no other move that can be made).

    :param board: Game board.

    :return: Boolean indicating if the game is tied.
    """
    return all((board != 0).flatten())

