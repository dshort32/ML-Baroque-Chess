'''WinningChessPlayer.py

'''

import math
import time
from random import randrange
import BC_state_etc as BC
import GenericBaroqueChessAgent as Agent

def makeMove(currentState, currentRemark, timelimit):
    start_time = time.time()

    valid_moves = Agent.available_moves(currentState)
    best_move = valid_moves[0]
    state_to_return = Agent.move_piece(currentState, best_move)
    for move in valid_moves:
        next_state = Agent.move_piece(currentState, move)

        # Pick the best move in the order of static_eval function
        if staticEval(next_state) > staticEval(state_to_return):
            best_move = move
            state_to_return = next_state

    newRemark = "Just taking a move"
    '''
    eval = alpha_beta(currentState, staticEval(currentState), 5, -math.inf, math.inf, True, start_time. timelimit)
    moves = available_moves(currentState)
    for move in moves :
        next_state = move_piece(currentState, move)
        if staticEval(next_state) == eval :
            return [[move, next_state], newRemark]

    return [[best_move, state_to_return], newRemark]
    '''
    return [[best_move, state_to_return], newRemark]

def alpha_beta(current_state, s_eval, depth, alpha, beta, max_player, begin_time, time_limit) :
    if time.time() > begin_time + time_limit :
        return s_eval
    if depth == 0 :
        return staticEval(currentState)
    if max_player :
        eval = -math.inf
        moves = available_moves(current_state)
        for move in moves :
            next_state = move_piece(current_state, move)
            eval = max(eval, alpha_beta(next_state, staticEval(next_state), depth - 1, alpha, beta, False, begin_time, time_limit))
            alpha = max(alpha, eval)
            if alpha >= beta : # beta cutoff
                break
        return eval
    else :
        eval = math.inf
        moves = available_moves(current_state)
        for move in moves :
            next_state = move_piece(current_state, move)
            eval = min(eval, alpha_beta(next_state, staticEval(next_state), depth - 1, alpha, beta, True, begin_time, time_limit))
            beta = min(beta, eval)
            if alpha >= beta :
                break # alpha cutoff
        return eval

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


def basic_make_move_test():
    timelimit = 1000 # 1000 seconds
    currentState = BC.BC_state()
    state_info, utterance = makeMove(currentState, "First Move", timelimit)
    move, newState = state_info
    print("===============================")
    print("  Chosen Move: "+str(move))
    print("===============================")
    print(str(newState))

if __name__ == '__main__':
    basic_make_move_test()
