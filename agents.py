from utils import Board
from abc import ABC, abstractclassmethod
from random import choice




class PlayerTemplate(ABC):
    
    @abstractclassmethod
    def _available_moves(self):
        pass
    
    @abstractclassmethod
    def make_move(self):
        pass
    
    @abstractclassmethod
    def get_name(self):
        pass
    
    @abstractclassmethod
    def get_piece(self):
        pass

class RandomPlayer(PlayerTemplate):
    def __init__(self, piece):
        self.__name = "Random"
        self.__piece = piece

    @staticmethod
    def _available_moves(board: Board) -> list:
        """
            Verifies the possible moves available on the board.

            Inputs:
                board: board where the game is played.
            returns: 
                list of available cells to play.
        """
        return [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == ' ']

    def make_move(self, board: Board) -> tuple:
        """
            Selects a random cell out of the ones available to play.
                Inputs:
                    board: board where the game is played.
                returns: 
                    tuple containing the coordinates of the cell where the agent is going to play.
        """
        return choice(self._available_moves(board))

    def get_name(self) -> str:
        """
            Returns the name of the player.
            return: Name of the player.
        """
        return self.__name
    
    def get_piece(self) -> str:
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