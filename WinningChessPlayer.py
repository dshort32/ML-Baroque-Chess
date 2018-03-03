'''WinningChessPlayer.py
'''

import BC_state_etc as BC
import time
import random

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    time.clock()
    locations = []
    board = currentState.board
    for row in range(len(board)) :
        for column in range(len(board[row])) :
            item = board[row][column]
            loc = row, column
            if currentState.whose_move == 0 and "a" <= item <= "z" :
                locations.append(loc)
            elif currentState.whose_move == 1 and "A" <= item <= "Z" :
                locations.append(loc)
    piece_loc = locations[random.randint(0, len(locations) - 1)]
    piece_row = piece_loc[0]
    piece_column = piece_loc[1]
    piece = board[piece_row][piece_column]
    if piece == 'p' :
        move = movePawn(piece_loc, 1)
    elif piece == 'P' :
        move = movePawn(piece_loc, -1)
    elif "a" <= piece <= "z" :
        move = moveOther(board, locations, piece, piece_loc)
    else :
        move = moveOther(board, locations, piece, piece_loc)


    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

def moveOther(board, locations, piece, piece_location) :
    directions = []
    piece_row = piece_location[0]
    piece_column = piece_location[1]
    for row in range(0, 2) :
        for column in range(0, 2) :
            if 0 <= piece_row + row - 1 < len(board) and 0 <= piece_column + column - 1 < len(board[0])\
                and board[row][column] == '-' :
                direction = row - 1, column - 1
                directions.append(direction)
    if len(directions) == 0 :
        movePawn(board, locations[random.randint(0, len(locations) / 2)])
    direction = directions[random.randint(0, len(directions) - 1)]
    row_direction = direction[0]
    column_direction = direction[1]
    current_loc = piece_location
    current_loc[0] += row_direction
    current_loc[1] += column_direction
    while 0 <= current_loc[0] < len(board) and 0 <= current_loc[1] < len(board[1])\
        and board[current_loc[0]][current_loc[1]] == '-' :
        locations.append(current_loc)
        current_loc[0] += row_direction
        current_loc[1] += column_direction
    new_loc = locations[random.randint(0, len(locations) - 1)]
    return piece_location, new_loc

def movePawn(board, piece_location, direction) :
    locations = []
    current_loc = piece_location
    current_loc[0] += direction
    while 0 <= current_loc[0] < len(board) and 0 <= current_loc[1] < len(board[1])\
        and board[current_loc[0]][current_loc[1]] == '-' :
        locations.append(current_loc)
        current_loc[0] += direction
    new_loc = locations[random.randint(0, len(locations) - 1)]
    return piece_location, new_loc

def nickname():
    return "Newman"

def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."

def prepare(player2Nickname):
    pass
