def player_won(player, board):
    """
    Verifies if the game has been won by the player by checking if there is tree consecutive marks from the same
    plater in any of the row, columns or diagonals.

    :param player: Mark of the player in the board.
    :param board: Game board.

    :return: Boolean indicating if the game has been won by the player.
    """
    # Checks the main diagonal
    main_diagonal = lambda board, marker: all([marker == board[i, i] for i in range(board.shape[0])])
    # Checks the secondary diagonal
    secondary_diagonal = lambda board, marker: all([marker == board[i, 2 - i] for i in range(board.shape[0])])
    # Checks the columns
    columns = lambda board, marker: any((True for row in board.T if all(row == marker)))
    # Checks the rows
    rows = lambda board, marker: any((True for row in board if all(row == marker)))

    if any(main_diagonal(board, player), secondary_diagonal(board, player),
           columns(board, player), rows(board, player)):
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
