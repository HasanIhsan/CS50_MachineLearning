# Program Name: TicTacToe
# Programmer: Hassan Ihsan
# objective: contains all the helper functions used in runner.py (simply put the backend of the game)

import math

# Constants representing players and empty cells
X = "X"
O = "O"
EMPTY = None

"""
Name: initial_state
Purpose: Returns the starting state of the board.

    Pseudo Code:
    return a 3x3 grid filled with EMPTY values
"""
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

"""
Name: player
Purpose: Determines which player's turn it is.

    Pseudo Code:
    count X and O occurrences on the board
    if X count <= O count, return X (X goes first)
    otherwise, return O
"""
def player(board):
    x_count = sum(row.count(X) for row in board)  # Count Xs on the board
    o_count = sum(row.count(O) for row in board)  # Count Os on the board
    return X if x_count <= o_count else O  # X starts first, then players alternate

"""
Name: actions
Purpose: Returns all possible moves.

    Pseudo Code:
    iterate through board cells
    if cell is EMPTY, add (i, j) to the set of possible moves
"""
def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

"""
Name: result
Purpose: Returns a new board with the given move applied.

    Pseudo Code:
    check if action is valid (cell must be EMPTY)
    create a deep copy of the board
    place current player's mark in the given position
    return the new board
"""
def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action")  # Ensure the move is valid
    
    new_board = [row[:] for row in board]  # Create a deep copy of the board
    new_board[i][j] = player(board)  # Assign the move to the current player
    return new_board

"""
Name: winner
Purpose: Determines if there is a winner.

    Pseudo Code:
    check each row, column, and diagonal for three matching marks
    if found, return the corresponding player
    otherwise, return None
"""
def winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]  # Row win
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]  # Column win
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    return None  # No winner yet

"""
Name: terminal
Purpose: Checks if the game is over.

    Pseudo Code:
    if there is a winner, return True
    if all cells are filled, return True
    otherwise, return False
"""
def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

"""
Name: utility
Purpose: Returns the utility value of a terminal state.

    Pseudo Code:
    if X won, return 1
    if O won, return -1
    otherwise, return 0
"""
def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

"""
Name: minimax
Purpose: Determines the optimal move using the Minimax algorithm.

    Pseudo Code:
    if board is terminal, return None
    determine current player
    for each possible action:
        simulate result of action
        evaluate move using min_value or max_value
        update best move accordingly
    return best move
"""
def minimax(board):
    if terminal(board):
        return None  # No move if game is over
    
    current_player = player(board)
    best_action = None
    
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
    
    return best_action

"""
Name: max_value
Purpose: Computes the max value for the Minimax algorithm.

    Pseudo Code:
    if board is terminal, return utility value
    set initial value to negative infinity
    for each action:
        get the min_value of the result board
        update value if greater
    return value
"""
def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf  # Worst case for maximizing player
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


"""
Name: min_value
Purpose: Computes the min value for the Minimax algorithm.

    Pseudo Code:
    if board is terminal, return utility value
    set initial value to positive infinity
    for each action:
        get the max_value of the result board
        update value if smaller
    return value
"""
def min_value(board):
    if terminal(board):
        return utility(board)
    value = math.inf  # Worst case for minimizing player
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value
