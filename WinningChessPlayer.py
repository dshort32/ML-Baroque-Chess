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

    # Author: Aaron
    available_moves = available_moves(currentState)
    best_move = available_moves[0]
    state_to_return = move_piece(currentState, best_move)
    for move in available_moves:
        next_state = move_piece(newState, move)
        if staticEval(next_state) > staticEval(state_to_return):
            best_move = move
            state_to_return = next_state

    return [[best_move, state_to_return], newRemark]

# Author: Aaron
def move_piece(currentState, move, capture_mode=True):
    # make copy
    turn = currentState.whose_move
    next_state = BC.BC_state(currentState.board, turn)
    if capture_mode:
        next_state.whose_move = 1 - currentState.whose_move

    start, end = move
    piece = next_state.board[start[0]][start[1]]
    next_state.board[start[0]][start[1]] = 0
    next_state.board[end[0]][end[1]] = piece
    if capture_mode:
        remove_captured(next_state, move)
    return next_state


# NEEDS IMPLEMENTATION
def remove_captured(state_to_update, move):
    board = state_to_update.board
    start, end = move
    moved_piece = board[end[0]][end[1]]
    player = BC.who(moved_piece)
    opponent = 1 - player
    removed_pieces = []
    if moved_piece == BC.BLACK_WITHDRAWER or moved_piece == BC.WHITE_WITHDRAWER:
        delta_i = end[0] - start[0]
        delta_j = end[1] - start[1]
        target_i = 0 if delta_i == 0 else start[0] - (delta_i) / abs(delta_i)
        target_j = 0 if delta_j == 0 else start[1] - (delta_j) / abs(delta_j)
        removed_location = target_i, target_j
        if inbounds(state_to_update, removed_location)\
            and BC.who(board[target_i][target_j]) == opponent\
            and board[target_i][target_j] != 0:
            removed_piece = board[target_i][target_j]
            board[target_i][target_j] = 0
            removed_pieces.append((removed_piece, removed_location))
    elif moved_piece == BC.BLACK_PINCER or moved_piece == BC.WHITE_PINCER:
        for pos in [(1,0),(-1,0),(0,1),(0,-1)]:
            target_i = end[0] + pos[0]
            target_j = end[1] + pos[1]
            pos_across= end[0] + 2 * pos[0], end[1] + 2 * pos[1]
            removed_location = target_i, target_j
            if inbounds(state_to_update, removed_location)\
                and inbounds(state_to_update, pos_across)\
                and BC.who(board[target_i][target_j]) == opponent\
                and board[target_i][target_j] != 0\
                and BC.who(board[pos_across[0]][pos_across[1]]) == player:
                removed_piece = board[target_i][target_j]
                board[target_i][target_j] = 0
                removed_pieces.append((removed_piece, removed_location))
    elif moved_piece == BC.BLACK_COORDINATOR or moved_piece == BC.COORDINATOR:
        kingPos = (0, 0)
        for i, row in board:
            for j, piece in row:
                if (piece == BC.BLACK_KING or piece == BC.WHITE_KING)\
                    and BC.who(piece) == player:
                    kingPos = (i,j)
                    break;

        # ERROR MUST BE FIXED
        for target_pos in [(end[0], kingPos[1]), (kingPos[0], end[1])]:
            if BC.who(board[target_pos[0]][target_pos[1]]) == opponent:
                removed_piece = board[[target_pos[0]][target_pos[1]]
                print(str(0))
                board[target_pos[0]][target_pos[1]] = 0
                removed_pieces.append((removed_piece, removed_location))
    elif moved_piece == BC.BLACK_LEAPER or moved_piece == BC.LEAPER:
        # HAVE NOT BEEN TESTED
        delta_i = end[0] - start[0]
        delta_j = end[1] - start[1]
        target_i = 0 if delta_i == 0 else end[0] - (delta_i) / abs(delta_i)
        target_j = 0 if delta_j == 0 else end[1] - (delta_j) / abs(delta_j)
        removed_location = target_i, target_j
        if inbounds(state_to_update, removed_location)\
            and BC.who(board[target_i][target_j]) == opponent\
            and board[target_i][target_j] != 0:
            removed_piece = board[target_i][target_j]
            board[target_i][target_j] = 0
            removed_pieces.append((removed_piece, removed_location))
    elif moved_piece == BC.BLACK_IMITATOR or moved_piece == BC.IMITATOR:
        '''shit'''

    return removed_pieces

# Author: Aaron
def available_moves(currentState):
    # Copy the state and the board
    turn = currentState.whose_move
    initialStateCopied = BC.BC_state(currentState.board, turn)
    available_move_list = []
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            currPos = (i,j)
            # If not your piece or frozen, don't do anything
            if (BC.who(piece) == BC.BLACK and turn == BC.WHITE)\
                or (BC.who(piece) == BC.WHITE and turn == BC.BLACK)\
                or isFrozen(initialStateCopied, currPos) or (piece == 0):
                continue
            if piece == BC.BLACK_KING or piece == BC.WHITE_KING:
                # Adding King's moves
                for i_k in range(-1, 2) :
                    for j_k in range(-1, 2) :
                        newPos = (i + i_k, j + j_k)
                        if location_available(initialStateCopied, newPos):
                            move = currPos, newPos
                            available_move_list.append(move)
            else:
                if piece != BC.BLACK_PINCER and piece != BC.WHITE_PINCER:
                    # Diagonal moves (Queen style moves)
                    recursive_find_moves(initialStateCopied, currPos, currPos, 1, 1, available_move_list)
                    recursive_find_moves(initialStateCopied, currPos, currPos, 1, -1, available_move_list)
                    recursive_find_moves(initialStateCopied, currPos, currPos, -1, 1, available_move_list)
                    recursive_find_moves(initialStateCopied, currPos, currPos, -1, -1, available_move_list)
                # Rook like moves
                recursive_find_moves(initialStateCopied, currPos, currPos, 0, 1, available_move_list)
                recursive_find_moves(initialStateCopied, currPos, currPos, 0, -1, available_move_list)
                recursive_find_moves(initialStateCopied, currPos, currPos, 1, 0, available_move_list)
                recursive_find_moves(initialStateCopied, currPos, currPos, -1, 0, available_move_list)

    return available_move_list

def isFrozen(state, position):
    opponent = 1 - state.whose_move
    for i_k in range(-1, 2) :
        for j_k in range(-1, 2) :
            i, j = position[0] + i_k, position[1] + j_k
            if not inbounds(state, (i, j)) or position == (i, j):
                continue
            currentPiece = state.board[position[0]][position[1]]
            adjacent_piece = state.board[i][j]
            if (adjacent_piece == BC.BLACK_FREEZER and opponent == BC.BLACK)\
                or (adjacent_piece == BC.WHITE_FREEZER and opponent == BC.WHITE)\
                or (currentPiece == BC.BLACK_FREEZER and adjacent_piece == BC.WHITE_IMITATOR)\
                or (currentPiece == BC.WHITE_FREEZER and adjacent_piece == BC.BLACK_IMITATOR):
                return True
    return False

def location_available(state, square):
    board = state.board
    i, j = square # (i, j)
    return inbounds(state, square) and board[i][j] == 0

def inbounds(state, square):
    board = state.board
    i, j = square # (i, j)
    return i >= 0 and i < len(board) and j >= 0 and j < len(board[0])

# Author: Aaron
def recursive_find_moves(currState, startPos, currPos, delta_i, delta_j, available_move_list):
    board = currState.board
    curRow, curCol = currPos
    newPosition = curRow + delta_i, curCol + delta_j
    curPiece = board[curRow][curCol]

    if location_available(currState, newPosition):
        move = (startPos, newPosition)
        nextState = move_piece(currState, (currPos, newPosition), False) # False: b/c We don't want capture_mode
        available_move_list.append(move)
        recursive_find_moves(nextState, startPos, newPosition, delta_i, delta_j, available_move_list)
    # Leaper's and Imitator's movements
    elif inbounds(currState, newPosition):
        leapPos = curRow + 2 * delta_i, curCol + 2 * delta_j
        piece_to_jump = currState.board[newPosition[0]][newPosition[1]]
        opponenet = 1 - currState.whose_move

        # Checks:   1. is location empty?
        #           2. is the piece to jump opponents?
        #           3. is your piece a Leaper?
        #           4. is your piece a Imitator with the opponents a Leaper?
        if location_available(currState, leapPos) and BC.who(piece_to_jump) == opponenet\
            and (curPiece == BC.BLACK_LEAPER or curPiece == BC.WHITE_LEAPER\
                or (curPiece == BC.BLACK_IMITATOR and piece_to_jump == BC.WHITE_LEAPER )\
                 or (curPiece == BC.WHITE_IMITATOR and piece_to_jump == BC.BLACK_LEAPER)):
            move = (startPos, leapPos)
            available_move_list.append(move)

def nickname():
    return "Winner"

def introduce():
    return "I'm Winner. I am decent at playing chess."

def prepare(player2Nickname):
    pass

# Author: Aaron
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

board = BC.parse('''
c l i w k i l f
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - C - w - - -
- - - - - - - -
- - p - p - - -
- - p - K - - -
''')

def basic_movement_test():
    currentState = BC.BC_state(board, BC.BLACK)
    print(currentState)
    moves = available_moves(currentState)
    print(len(moves))
    for m in moves:
        start, end = m
        piece = BC.CODE_TO_INIT[currentState.board[start[0]][start[1]]]
        print("p: "+str(piece)+" s: "+str(start)+" t: "+str(end))

if __name__ == '__main__':
   # Create the currentState and ask this agent to make a moves

   currentState = BC.BC_state(board, BC.WHITE)
   print(currentState)
   move = ((4,0), (4, 2))
   remove_captured(currentState, move)
   print(currentState)

   # timelimit = 1000
   # state_info, utterance = makeMove(currentState, "First Move", timelimit)
   # move, newState = state_info
   # print("move: "+str(move))
   # print(str(newState))
