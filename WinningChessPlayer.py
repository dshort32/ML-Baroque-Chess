'''WinningChessPlayer.py

'''

import math
import time
from random import randrange
import BC_state_etc as BC
import GenericBaroqueChessAgent as Agent

PIECE_TO_VAL = {0: 0, 2:10, 3:10, 4:30, 5:30, 6:40, 7:40, 8:80, 9:80,
  10:80, 11:80, 12:1000, 13:1000, 14:80, 15:80}

def makeMove(currentState, currentRemark, timelimit):
    end_time = time.time() + timelimit # in seconds

    depth = 0
    best_move = Agent.available_moves(currentState)[0]
    state_to_return = Agent.move_piece(currentState, best_move)
    while time.time() < end_time:
        evaluated, best_move = alpha_beta(currentState, depth, -math.inf, math.inf, True, end_time)

    newRemark = "Here it is. Shit"
    return [[best_move, state_to_return], newRemark]

def alpha_beta(current_state, depth, alpha, beta, max_player, end_time):
    moves = Agent.available_moves(current_state)
    best_move = moves[0]
    if time.time() > end_time or depth == 0 or len(moves) == 0:
        return (staticEval(current_state), None)
    if max_player:
        evaluated = -math.inf

        for move in moves :
            next_state = Agent.move_piece(current_state, move)
            result, child_move = alpha_beta(next_state, depth - 1, alpha, beta, False, end_time)
            # evaluated = max(evaluated, result)
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
            # evaluated = min(evaluated, result)
            if result < evaluated:
                evaluated = result
                best_move = move
            beta = min(beta, evaluated)
            if alpha >= beta :
                break # alpha cutoff
    return evaluated, best_move

def getStateHash(state):
    return (str(state)).__hash__()

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
            val = PIECE_TO_VAL[piece]
            if BC.who(piece) == BC.WHITE:
                static_val += val
            else:
                static_val -= val
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

b2 = BC.parse('''
- - - - - - - k
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
F F F - - - - -
i i i - - - - -
- - L - - - - K
''')
if __name__ == '__main__':
    # basic_make_move_test()
    currentState = BC.BC_state(INITIAL, BC.BLACK)
    end_time = time.time() + 2 # in seconds

    evaluated, move = alpha_beta(currentState, 5, -math.inf, math.inf, True, end_time)
    print("CONCLUSION: "+str(evaluated))
    print("Move: "+str(move))

    '''
    nother = BC.BC_state(b2, BC.WHITE)
    print("B1: "+str(staticEval(currentState)))
    print("B2: "+str(staticEval(nother)))
    policy[getStateHash(currentState)] = "a"
    policy[getStateHash(b2)] = "b"
    '''
