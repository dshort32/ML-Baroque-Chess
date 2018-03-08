'''AlphaBetaPlayer.py

'''

import math
import time
from random import randint
import BC_state_etc as BC
import GenericBaroqueChessAgent as Agent

PIECE_TO_VAL = {0: 0, 2:-10, 3:10, 4:-30, 5:30, 6:-40, 7:40, 8:-80, 9:80,
  10:-80, 11:80, 12:-10000, 13:10000, 14:-80, 15:80}

NUM_TURNS_TAKEN = 0
MOVE_QUEUE = [(0,((0, 0),(0, 0))) for i in range(10)]

def makeMove(currentState, currentRemark, timelimit):
    global NUM_TURNS_TAKEN, MOVE_QUEUE
    end_time = time.time() + timelimit - 0.5 # in seconds
    NUM_TURNS_TAKEN += 1
    depth = 0

    valid_moves = Agent.available_moves(currentState)
    best_move = valid_moves[0]
    while time.time() < end_time:
        evaluated, best_move = alpha_beta(currentState, depth, -math.inf, math.inf, True, end_time)
        depth += 1

    newRemark = "Here it is. Shit"
    piece = currentState.board[best_move[0][0]][best_move[0][1]]
    if (piece, best_move) in MOVE_QUEUE:
        random_i = randint(0, len(valid_moves) - 1)
        best_move = valid_moves[random_i]
        piece = currentState.board[best_move[0][0]][best_move[0][1]]

    MOVE_QUEUE[NUM_TURNS_TAKEN % len(MOVE_QUEUE)] = (piece, best_move)
    state_to_return = Agent.move_piece(currentState, best_move)
    return [[best_move, state_to_return], newRemark]

def alpha_beta(current_state, depth, alpha, beta, max_player, end_time):
    moves = Agent.available_moves(current_state)
    # moves = Agent.order(current_state, moves)
    best_move = moves[0]
    if time.time() > end_time or depth == 0 or len(moves) == 0:
        return (staticEval(current_state), best_move)
    if max_player:
        evaluated = -math.inf

        for move in moves :
            next_state = Agent.move_piece(current_state, move)
            result, child_move = alpha_beta(next_state, depth - 1, alpha, beta, False, end_time)
            if result > evaluated:
                evaluated = result
                best_move = move
            alpha = max(alpha, evaluated)
            if alpha >= beta : # beta cutoff
                break
    else:
        evaluated = math.inf
        for move in moves :
            next_state = Agent.move_piece(current_state, move)
            result, child_move = alpha_beta(next_state, depth - 1, alpha, beta, True, end_time)
            if result < evaluated:
                evaluated = result
                best_move = move
            beta = min(beta, evaluated)
            if alpha >= beta :
                break # alpha cutoff
    return evaluated, best_move

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

    # Calculating next_to_enemy_piece
    for i, row in enumerate(state.board):
        for j, piece in enumerate(row):
            currPieceOwner = BC.who(piece)
            static_val += PIECE_TO_VAL[piece] # Living bonus

    return static_val


def basic_make_move_test():
    timelimit = 2 # 1000 seconds
    currentState = BC.BC_state()
    state_info, utterance = makeMove(currentState, "First Move", timelimit)
    move, newState = state_info
    print("===============================")
    print("  Chosen Move: "+str(move))
    print("===============================")
    print(str(newState))


INITIAL = BC.parse('''
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
    # basic_make_move_test()

    currentState = BC.BC_state(INITIAL, BC.BLACK)
    print("val: "+str(staticEval(currentState)))

    end_time = time.time() + 10 # in seconds

    evaluated, move = alpha_beta(currentState, 2, -math.inf, math.inf, True, end_time)
    print(currentState)
    lol = staticEval(Agent.move_piece(currentState, move))
    print("CONCLUSION: "+str(evaluated))
    print("val: "+str(lol))
    print("Move: "+str(move))


    '''
    nother = BC.BC_state(b2, BC.WHITE)
    print("B1: "+str(staticEval(currentState)))
    print("B2: "+str(staticEval(nother)))
    policy[getStateHash(currentState)] = "a"
    policy[getStateHash(b2)] = "b"
    '''
