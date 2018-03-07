'''CrazyChessDude.py

This player just chooses a random move possible.
'''

import time
from random import randint
import BC_state_etc as BC
import GenericBaroqueChessAgent as Agent

def makeMove(currentState, currentRemark, timelimit):
    start_time = time.time()

    valid_moves = Agent.available_moves(currentState)
    if len(valid_moves) == 0:
        return None, "I believe I have no legal moves."
    elif len(valid_moves) == 1:
        best_move = valid_moves[0]
    else:
        random_i = randint(0, len(valid_moves) - 1)
        best_move = valid_moves[random_i]
    state_to_return = Agent.move_piece(currentState, best_move)
    newRemark = "Just taking a move"
    return [[best_move, state_to_return], newRemark]

def nickname():
    return "CrazyDude"

def introduce():
    return "I'm CrazyChessDude.  I mostly just move whatever piece is able to move."

def prepare(player2Nickname):
    pass

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
