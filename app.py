import random

game_states = ('Game not finished', 'Draw', 'X wins', 'O wins')
game_levels = ('easy', 'medium', 'expert')

win_positions = [(0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
bd = {'1 3': 0, '2 3': 1, '3 3': 2,
      '1 2': 3, '2 2': 4, '3 2': 5,
      '1 1': 6, '2 1': 7, '3 1': 8,
      }
opp_turn = {'X': 'O', 'O': 'X'}

board = '_' * 9


def render_grid():
    b = board.replace('_', ' ')
    print('-' * 9)
    print("| {} {} {} |".format(b[0], b[1], b[2]))
    print("| {} {} {} |".format(b[3], b[4], b[5]))
    print("| {} {} {} |".format(b[6], b[7], b[8]))
    print('-' * 9)


def get_game_state():
    x_wins = any(all((board[index] == 'X') for index in each_tuple) for each_tuple in win_positions)
    o_wins = any(all((board[index] == 'O') for index in each_tuple) for each_tuple in win_positions)
    game_not_finished = '_' in board
    draw = '_' not in board
    if x_wins:
        return 'X wins'
    elif o_wins:
        return 'O wins'
    elif game_not_finished:
        return 'Game not finished'
    elif draw:
        return 'Draw'


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


def is_move_possible(m):
    # Check if all inputs are digits
    is_digit = [(item.isdigit() or item == ' ') for item in m]
    if not all(is_digit):
        print('You should enter numbers!')
        return False

    # Check if all digits are within the right range
    is_within_range = [(item == ' ' or 0 < (int(item) < 4)) for item in m]
    if not all(is_within_range):
        print('Coordinates should be from 1 to 3!')
        return False

    # Check if cell is occupied
    index = bd[m]
    if board[index] != '_':
        print('This cell is occupied! Choose another one!')
        return False

    return True


def process_user_move(m):
    global board
    # Make move
    index = bd[m]
    b = list(board)
    turn = 'O'
    if b.count('X') <= b.count('O'):
        turn = 'X'
    b[index] = turn
    return ''.join(b)


def process_computer_move(index):
    b = list(board)
    turn = 'O'
    if board.count('X') <= board.count('O'):
        turn = 'X'
    b[index] = turn
    return ''.join(b)


def comp_easy_move():
    # Find a random move from all available moves
    available_moves = []
    for i in range(9):
        if board[i] == '_':
            available_moves.append(i)
    return random.choice(available_moves)


def comp_medium_move():
    # Getting which symbol is the next turn
    turn = 'O'
    if board.count('X') <= board.count('O'):
        turn = 'X'

    # If there is a winning move
    for tup in win_positions:
        board_pieces = ''.join([board[index] for index in tup])
        if board_pieces.count(turn) == 2 and '_' in board_pieces:
            move = board_pieces.index('_')
            move = tup[move]
            return move

    # If opponent has a winning move
    for tup in win_positions:
        board_pieces = ''.join([board[index] for index in tup])
        if board_pieces.count(opp_turn[turn]) == 2 and '_' in board_pieces:
            move = board_pieces.index('_')
            move = tup[move]
            return move

    # If first 2 are not possible
    return comp_easy_move()


def find_available_spots(b):
    available_moves = []
    for i in range(9):
        if b[i] == '_':
            available_moves.append(i)
    return available_moves


def get_board_point(b, turn):
    if (get_game_state_list(b) == 'X wins' and turn == 'X') or (
            get_game_state_list(b) == 'O wins' and turn == 'O'):
        return 10

    elif (get_game_state_list(b) == 'O wins' and turn == 'X') or (
            get_game_state_list(b) == 'X wins' and turn == 'O'):
        return -10

    elif get_game_state_list(b) == 'Draw':
        return 0


def mini_max(b, turn):
    # print(f'Function called -> {board} -> {turn}')
    working_board = [piece for piece in b]
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


def comp_hard_move():
    # Getting which symbol is the next turn
    turn = 'O'
    if board.count('X') <= board.count('O'):
        turn = 'X'
    if board.count('_') == 9:
        return comp_easy_move()
    return mini_max(board, turn)


def game(player_1, player_2):
    global board
    render_grid()
    # makes sure that player 1 plays first
    playing = player_1

    while get_game_state() == 'Game not finished':

        # Deciding how to receive input from active player
        if playing == 'user':
            move = input("Enter the coordinates: ")
            while not is_move_possible(move):
                move = input("Enter the coordinates: ")
            board = process_user_move(move)
        elif playing == 'easy':
            print('Making move level "easy"')
            board = process_computer_move(comp_easy_move())
        elif playing == 'medium':
            print('Making move level "medium"')
            board = process_computer_move(comp_medium_move())
        elif playing == 'hard':
            print('Making move level "hard"')
            board = process_computer_move(comp_hard_move())
        render_grid()

        # Switching to the next player
        if playing == player_1:
            playing = player_2
        elif playing == player_2:
            playing = player_1

    print(get_game_state())

    # Resetting the game board at the end of the game
    board = '_' * 9


def menu():
    command = (input('Input command: ')).split(' ')
    while command[0] != 'exit':
        if len(command) != 3:
            print("Bad parameters!")
            command = (input('Input command: ')).split(' ')
        else:
            player_1 = command[1]
            player_2 = command[2]
            game(player_1, player_2)
            print()
            command = (input('Input command: ')).split(' ')


menu()
