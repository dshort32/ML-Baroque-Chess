'''WinningChessPlayer.py

'''

import math
import time
from random import randrange
import BC_state_etc as BC

def makeMove(currentState, currentRemark, timelimit):
    start_time = time.time()
    print

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)


    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

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

def available_moves(state, position):
    '''
    board = [row[:] for row in state.board]
    row, col = position
    piece = board[row][col]
    available_move_list = []
    if piece == BLACK_KING or piece == WHITE_KING:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i >= 0 or i < len(board) or j >= 0 or j < len(board[0]))\
                    and (board[i][j] == 0 or isKingInDanger): # inbounds and (empty or can take without being in danger)
                    available_move_list.append((i, j))
    elif piece == BLACK_PINCER or piece == WHITE_PINCER:
    '''

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
