'''WinningChessPlayer.py

'''

import time
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


if __name__ == '__main__':
   # Create the currentState and ask this agent to make a moves
   currentState = BC.BC_state()
   timelimit = 1000
   makeMove(currentState, "First Move", timelimit)
