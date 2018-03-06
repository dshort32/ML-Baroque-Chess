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

    best_move = valid_moves[0]
    evaluated = alpha_beta(currentState, 20, -math.inf, math.inf, True, end_time)
    moves = available_moves(currentState)
    for move in moves :
        next_state = move_piece(currentState, move)
        if staticEval(next_state) == evaluated :
            return [[move, next_state], newRemark]

    return [[best_move, state_to_return], newRemark]

def alpha_beta(current_state, depth, alpha, beta, max_player, end_time):
    moves = Agent.available_moves(current_state)
    if time.time() > end_time or depth == 0 or len(moves) == 0:
        return staticEval(currentState)
    if max_player:
        evaluated = -math.inf

        for move in moves :
            next_state = Agent.move_piece(current_state, move)
            '''
            string = ""
            for i in range(0, 2 - depth):
                string += " "
            print(string+"WHITE: "+str(move))

            string = ""
            for i in range(0, 3 - depth):
                string += " "
            print(string+BC.CODE_TO_INIT[next_state.board[move[1][0]][move[1][1]]]+" - "+str(move))
            '''
            evaluated = max(evaluated, alpha_beta(next_state, depth - 1, alpha, beta, False, end_time))
            alpha = max(alpha, evaluated)
            if alpha >= beta : # beta cutoff
                break
    else:
        evaluated = math.inf
        for move in moves :
            next_state = Agent.move_piece(current_state, move)
            '''
            string = ""
            for i in range(0, 2 - depth):
                string += " "
            print(string+"BLACK: "+str(move))

            string = ""
            for i in range(0, 3 - depth):
                string += " "
            print(string+BC.CODE_TO_INIT[next_state.board[move[1][0]][move[1][1]]]+" - "+str(move))
            '''
            evaluated = min(evaluated, alpha_beta(next_state, depth - 1, alpha, beta, True, end_time))
            beta = min(beta, evaluated)
            if alpha >= beta :
                break # alpha cutoff

    return evaluated

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
- - - - - - - k
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
F F F - - - - -
i i i - - - - -
L p - - - - - K
''')
if __name__ == '__main__':
    # basic_make_move_test()
    currentState = BC.BC_state(INITIAL, BC.WHITE)
    end_time = time.time() + 20 # in seconds
    evaluated = alpha_beta(currentState, 10, -math.inf, math.inf, True, end_time)
    print("CONCLUSION: "+str(evaluated))
