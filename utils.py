import numpy as np
from agents import RandomPlayer
import time



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

    def place_piece(self, coordinates: tuple, piece: str):
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

class GameManager:
    @staticmethod
    def select_players() -> list:
        """
            Selects the players that will be playing the game.

            returns:
                List of classes, corresponding to the players.
        """
        players = {
            '1' : RandomPlayer
        }
        selected_players = []

        # Repeating until it has enough players.
        while len(selected_players) < 2:
            print("\n1. Random\n2. Greedy\n3. MinMax\n")
            input_ = input(f"Select the {len(selected_players) + 1}° player: ")

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
                board_state = board.get_board()
                # Making and placing the move.
                move = player.make_move(board_state)

                board.place_piece(move, piece)

                print(f"Player {piece} turn.")
                print(board)

                time.sleep(1)

                # Checking if the game is a tie
                if board.tie():
                    print("Game is a tie!")
                    game_ended = True
                    break

                # Checking if the game was won by the player
                elif board.player_won(piece):
                    print(f'{player.get_name()} won!')
                    game_ended = True
                    break

def one_move_win(piece: str, board: Board) -> int:
    '''
        Verifies the current board to obtain the amount of cases where there's one piece
        remaining to win.

        inputs:
                piece(str): Player's piece.
                board(Board): Current board. 
        Outputs:
                Amount of cases where there's only one piece remaining to win normalized.
    '''
    heuristic = 0
    # Filtering the diagonals
    main_diagonal = [board[(i, i)] for i in range(board.shape[0])]
    second_diagonal = [board[i, 2 - i] for i in range(board.shape[0])]

    can_win = lambda piece, row: 1 if (piece == row).sum() == 2 and (piece != row).sum() == 0 else 0

    for matrix in [board.get_board(), board.get_board().T]:
        for row in matrix:
            heuristic += can_win(piece, row)
    
    for diagonal in [main_diagonal, second_diagonal]:
        heuristic += can_win(piece, diagonal)

    return heuristic / 8