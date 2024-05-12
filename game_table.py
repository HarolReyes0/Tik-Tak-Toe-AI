import numpy as np

"""
   To do:
            
"""


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

      def __get_board(self):
            return self.__board

class Game(Board):
      def __init__(self):
            """
                  This method starts the game board and saves all rules.
            """
            self.__game_board = Board()

            # Checks if the player won
            self.__main_diagonal = lambda board, turn: all([turn == board[i, i] for i in range(board.shape[0])])
            self.__secondary_diagonal = lambda board, turn: all([turn == board[i, 2 - i] for i in range(board.shape[0])])
            self.__columns = lambda board, turn: any((True for row in board.T if all(row == turn)))
            self.__rows = lambda board, turn: any((True for row in board if all(row == turn)))

            # Checks if the game is a tie
            self.__tie = lambda board: all((board != 0).flatten())

      def start(self, player1, player2):
            pass