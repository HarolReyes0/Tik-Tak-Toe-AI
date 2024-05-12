import numpy as np

"""
   To do:
            Make a loop to play the game.
            Verify if any of the player won if so print who won.
            
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