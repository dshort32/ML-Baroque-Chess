
'''WinningChessPlayer.py

'''

import math
import time
from random import randrange
import BC_state_etc as BC

def makeMove(currentState, currentRemark, timelimit):
    start_time = time.time()

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    '''
    available_moves = available_moves(currentState)
    best_move = available_moves[0]
    state_to_return = move(currentState, best_move)
    for move in available_moves:
        next_state = move(newState, move)
        if staticEval(next_state) > staticEval(state_to_return):
            best_move = move
            state_to_return = next_state
    '''
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

    # return [[best_move, state_to_return], newRemark]



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

def move(currentState, move):
    next_state = BC.BC_state(currentState)
    next_state.whose_move = 1 - currentState.whose_move

    start, end = move
    piece = next_state.board[start[0]][start[1]]
    next_state.board[start[0]][start[1]] = 0
    next_state.board[end[0]][end[1]] = piece
    remove_captured(next_state)
    return next_state

# NEED MORE WORK
def available_moves(currentState):
    # Copy the state and the board
    initialStateCopied = BC.BC_state(currentstate)
    board = [row[:] for row in currentState.board]
    available_move_list = []
    for row in board:
        for piece in row:
            if piece == BLACK_KING or piece == WHITE_KING:

            elif piece == BLACK_PINCER or piece == WHITE_PINCER:

    return available_move_list

# NEED MORE WORK
def recursive_find_moves(board, position, delta_i, delta_j, available_move_list):
    curRow, curCol = position
    piece = board[curRow][curCol]
    nextRow = curRow + delta_i
    nextCol = curCol + delta_j
    if (nextRow >= 0 or nextRow < len(board) or nextCol >= 0 or nextCol < len(board[0]))\
        and (board[nextRow][nextCol] == 0):

            recursive_find_moves()
            available_move_list.append((i, j))


def nickname():
    return "Winner"

def introduce():
    return "I'm Winner. I am decent at playing chess."

def prepare(player2Nickname):
    pass

def staticEval(state):
    '''An enemy piece is -1 and my own piece is +1'''
    turn = state.whose_move
    static_val = 0
    for row in state.board:
        for piece in row:
            if piece != 0 and BC.who(piece) == BC.WHITE:
                static_val += 1
            elif piece != 0:
                static_val -= 1
    return static_val if turn == BC.WHITE else -static_val

# MIGHT NEED FOR ABOVE METHOD
def recursive_available_moves(board, position, delta_i, delta_j, available_move_list):
    '''
    row, col = position

    newR = row + delta_i
    newC = col + delta_j

    piece = board[row][col]
    turn = WHITE if piece % 2 == 0 else BLACK
    if newR < 0 or newR >= len(board) or newC < 0 or newC >= len(board[0])\
        (piece != 0 and ( piece == BLACK_KING or WHITE_KING )):
        return available_move_list
    newPlace = board[newR][newC]
    if piece == BLACK_KING or WHITE_KING:
        if newPlace == 0: # empty
            available_move_list.append((newR, newC))
            return available_move_list
        else if : # king can take the piece
            available_move_list.append((newR, newC))
            return available_move_list
        else:
            return avaiable_move_list
    '''

board = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')
if __name__ == '__main__':
   # Create the currentState and ask this agent to make a moves
   currentState = BC.BC_state(board, BC.WHITE)
   print(currentState)
   print("static eval: "+str(staticEval(currentState)))
   # timelimit = 1000
   # state_info, utterance = makeMove(currentState, "First Move", timelimit)
   # move, newState = state_info
   # print("move: "+str(move))
   # print(str(newState))
