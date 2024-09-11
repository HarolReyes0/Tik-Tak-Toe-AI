from GameEnviroment.GameBoard import Board
from GameEnviroment.Rules import player_won, tie


def play(player1, player2):
    board = Board()
    game_ended = False

    while not game_ended:
        for id_, player in enumerate([player1, player2]):
            # Getting the board state.
            board_state = board.get_board()
            # The agent picks a move based on the board state.
            move = player.make_a_move(board_state)

            # The move is added in the board.
            board.add_symbol(move, id_ + 1)
            print(board.see_board())

            # Checking if the game is a tie
            if tie(board_state):
                print("Game is a tie!")
                game_ended = True
                break

            # Checking if the game was won by the player
            elif player_won(id_ + 1, board_state):
                print(f'{player.get_name()} won!')
                game_ended = True
                break
