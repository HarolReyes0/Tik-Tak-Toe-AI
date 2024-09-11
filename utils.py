import numpy as np




class Board:
      """
      This class creates the game board, this board consist in a 3 x 3 matrix
      full of zeros.
      """
      def __init__(self):
            self.__board = np.zeros((3, 3), dtype=int)

      def see_board(self):
            """
            Prints the game board in an acsii style.
            """
            for idx, row in enumerate(self.__board):
                  print(f'{row[0]} | {row[1]} | {row[2]}')
                  if (idx + 1) % 3 != 0:
                        print('- + - + -')

      def add_symbol(self, coordinates, symbol):
            """
            Adds the symbol to the cell selected.

            Inputs:
                  coordinates: coordinates where the symbol is going to be placed.
                  symbol: symbol to be placed.
                          player 1: 1
                          player 2: 2
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

