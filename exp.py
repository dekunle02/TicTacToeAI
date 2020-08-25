"""
-find all available spots, know whose turn it is

-check score for each spot, and put it in a list
 choose the highest score.

- use the score to pick the index of the move, and return that

.. we have 2 possible moves, it checks first and realizes it will score -10 checks second and wins with that so +10
picks the score that is higher between the two and returns that index as the move

"""

win_positions = [(0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
opp_turn = {'X': 'O', 'O': 'X'}


def get_game_state_list(b):
    x_wins = any(all((b[index] == 'X') for index in each_tuple) for each_tuple in win_positions)
    o_wins = any(all((b[index] == 'O') for index in each_tuple) for each_tuple in win_positions)
    game_not_finished = '_' in b
    draw = '_' not in b
    if x_wins:
        return 'X wins'
    elif o_wins:
        return 'O wins'
    elif game_not_finished:
        return 'Game not finished'
    elif draw:
        return 'Draw'


def find_available_spots(board):
    available_moves = []
    for i in range(9):
        if board[i] == '_':
            available_moves.append(i)
    return available_moves


# Board = XX_XO_OO_
# Available spots = 0, 1, 4, 7, 8,  refers to the index on the board
# ---------
# |       |
# | X O   |
# |       |
# ---------

# ---------
# |   X   |
# | X O   |
# |   O   |
# ---------

#  X X   |
# | X O   |
# | O O


sample_board = "XX_XO_OO_"
sample_board2 = "___XO____"
sample_board3 = "_X_XO__O_"
sample_board4 = "XX_XO_OO_"


def get_board_point(board, turn):
    if (get_game_state_list(board) == 'X wins' and turn == 'X') or (
            get_game_state_list(board) == 'O wins' and turn == 'O'):
        return 10

    elif (get_game_state_list(board) == 'O wins' and turn == 'X') or (
            get_game_state_list(board) == 'X wins' and turn == 'O'):
        return -10

    elif get_game_state_list(board) == 'Draw':
        return 0


def mini_max(board, turn):
    # print(f'Function called -> {board} -> {turn}')
    working_board = [piece for piece in board]
    available_spots = find_available_spots(working_board)
    spot_points = []

    for spot in available_spots:
        working_board[spot] = turn

        spot_point = get_board_point(working_board, turn)

        looping_board = [item for item in working_board]
        while spot_point is None:
            opponent_turn = opp_turn[turn]
            opponent_move = mini_max(''.join(looping_board), opponent_turn)
            looping_board[opponent_move] = opponent_turn
            spot_point = get_board_point(looping_board, turn)

        working_board[spot] = '_'
        spot_points.append(spot_point)

    max_score = max(spot_points)
    move_position = available_spots[spot_points.index(max_score)]
    return move_position


"""
choose the highest score
    find its index
    move position = available_spots[index of highest mark]
    return move position
"""

print(mini_max(sample_board, 'X'))
print(mini_max(sample_board2, 'X'))
print(mini_max(sample_board3, 'X'))
print(mini_max(sample_board4, 'X'))
