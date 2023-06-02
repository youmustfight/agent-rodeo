# ==========================================================
# Tic-Tac-Toe Experiment
# Chat-based completion weaving into a tic tac toe game
# ==========================================================

def get_board_choices(board):
    choices = []
    for row_idx, row_abbrev in enumerate(['T','M','B']):
        for col_idx, col_abbrev in enumerate(['L','M','R']):
            if board[row_idx][col_idx] == None:
                choices.append(f'{row_abbrev}{col_abbrev}')
    return choices

def update_board(board, player_num, player_choice):
    row_idx = None
    col_idx = None
    if player_choice[0] == 'T': row_idx = 0
    if player_choice[0] == 'M': row_idx = 1
    if player_choice[0] == 'B': row_idx = 2
    if player_choice[1] == 'L': col_idx = 0
    if player_choice[1] == 'M': col_idx = 1
    if player_choice[1] == 'R': col_idx = 2
    if board[row_idx][col_idx] == None:
        update_board = board
        update_board[row_idx][col_idx] = player_num
        return update_board
    else:
        print("Picked a slot with an existing value")
        return board

def check_board_winner(board):
    # rows
    for row in board:
        if all(num == 1 for num in row): return 1
        if all(num == 2 for num in row): return 2
    # cols
    for col in [0, 1, 2]:
        if all(board[row][col] == 1 for row in [0, 1, 2]): return 1
        if all(board[row][col] == 2 for row in [0, 1, 2]): return 2
    # diagnols
    if all(pos_num == 1 for pos_num in [board[0][0], board[1][1], board[2][2]]): return 1
    if all(pos_num == 2 for pos_num in [board[0][0], board[1][1], board[2][2]]): return 2
    if all(pos_num == 1 for pos_num in [board[0][2], board[1][1], board[2][0]]): return 1
    if all(pos_num == 2 for pos_num in [board[0][2], board[1][1], board[2][0]]): return 2
    # nothing
    return None

def print_board(board, symbol_player_1, symbol_player_2):
    def get_symbol(num_player):
        if num_player == 1:
            return symbol_player_1
        if num_player == 2:
            return symbol_player_2
        return " "
    print(f'''
    {get_symbol(board[0][0])} | {get_symbol(board[0][1])} | {get_symbol(board[0][2])}
    - - - - -
    {get_symbol(board[1][0])} | {get_symbol(board[1][1])} | {get_symbol(board[1][2])}
    - - - - -
    {get_symbol(board[2][0])} | {get_symbol(board[2][1])} | {get_symbol(board[2][2])}
    ''')


def play():
    # SETUP BOARD & PLAYERS
    board = [
        [None,None,None],
        [None,None,None],
        [None,None,None],
    ]
    # --- inform players
    print('Lets play Tic Tac Toe!')
    symbol_player_1 = input('Symbol for player 1 (default X): ') or "X"
    symbol_player_2 = input('Symbol for player 1 (default O): ') or "O"
    print(f'Player 1: {symbol_player_1}')
    print(f'Player 2: {symbol_player_2}')

    # RUN GAME
    num_players_turn = 1
    while True:
        # --- if no more choices, end game in tie
        if len(get_board_choices(board)) == 0:
            print('Tie!')
            break
        # --- ask input
        round_choice = input(f'Player {num_players_turn}, choose a position ({", ".join(get_board_choices(board))}): ')
        # --- if a possible option...
        if round_choice in get_board_choices(board):
            # --- update board
            board = update_board(board, num_players_turn, round_choice)
            # --- show board
            print_board(board, symbol_player_1=symbol_player_1, symbol_player_2=symbol_player_2)
            # --- detmerine if we have a winner yet
            if check_board_winner(board) != None:
                print(f'Player {check_board_winner(board)} wins!')
                break
            # --- otherwise next round with next player
            num_players_turn = 2 if num_players_turn == 1 else 1 


if __name__ == '__main__':
    play()
