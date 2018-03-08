'''WinningChessPlayer.py

'''

import math
import time
from random import randint
from random import random
import BC_state_etc as BC
import GenericBaroqueChessAgent as Agent

Q_VALUE_FILE = "q_value.txt"
POLICY = {}
Q_VALUES = {}
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.7

def makeMove(currentState, currentRemark, timelimit):
    global POLICY
    # Switch white and black
    flag = False
    if currentState.whose_move == BC.BLACK:
        flag = True
        currentState = switchBlackAndWlhite(currentState)
    if currentState not in POLICY:
        valid_moves = Agent.available_moves(currentState)
        if len(valid_moves) == 0:
            return None, "I believe I have no legal moves."
        elif len(valid_moves) == 1:
            best_move = valid_moves[0]
        else:
            random_i = randint(0, len(valid_moves) - 1)
            best_move = valid_moves[random_i]
    else:
        best_move = POLICY[currentState]
    state_to_return = Agent.move_piece(currentState, best_move)
    if flag:
        state_to_return = switchBlackAndWlhite(currentState)
    newRemark = "HERE IT IS"
    return [[best_move, state_to_return], newRemark]

def nickname():
    return "Winner"

def introduce():
    return "I'm Winner. I am decent at playing chess."

def prepare(player2Nickname):
    # loadInfo()
    pass

def staticEval(state):
    '''An enemy piece is -1 and my own piece is +1'''
    turn = state.whose_move
    static_val = 0

    # Calculating next_to_enemy_piece
    for i, row in enumerate(state.board):
        for j, piece in enumerate(row):
            if piece != 0:
                if BC.who(piece) == turn:
                    static_val += 1
                else:
                    static_val -= 1


    return static_val

def loadInfo():
    global Q_VALUE_FILE, POLICY
    f = open(Q_VALUE_FILE, "r")
    policy = {}
    while True:
        state = f.read(64)
        action = f.read(4)
        if not state or not action:
            break

        # create state
        board = [[0,0,0,0,0,0,0,0] for r in range(8)]
        for v in range(64):
            i = int(v / 8)
            j = v % 8
            board[i][j] = int(state[v], 16)
        state = BC.BC_state(board, BC.WHITE)

        # craete move
        start_i = int(action[0],16)
        start_j = int(action[1],16)
        end_i = int(action[2],16)
        end_j = int(action[3],16)
        move = ((start_i, start_j), (end_i, end_j))

        # add policy
        policy[state] = move
    f.close()
    POLICY = policy

def saveInfo():
    global Q_VALUE_FILE, POLICY
    policy = POLICY
    f = open(Q_VALUE_FILE, "w")
    f.truncate(0)
    for state in policy.keys():
        string = ""

        # adding state info
        for row in state.board:
            for piece in row:
                string += format(piece, "X")

        # adding move info
        move = policy[state]
        string += format(move[0][0], "X")
        string += format(move[0][1], "X")
        string += format(move[1][0], "X")
        string += format(move[1][1], "X")

        # write the string
        val = f.write(string)
    f.close()

def hasLost(state, side = BC.WHITE):
    board = state.board
    for row in board:
        for piece in row:
            if (piece == 12 or piece == 13) and BC.who(piece) == side:
                return False
    return True

def learn(seconds):
    global POLICY, GAMMA, ALPHA, EPSILON
    end_time = time.time() + seconds
    POLICY = {}
    Q_VALUES = {}
    n = 0
    while end_time > time.time() and len(POLICY) < 1000000:
        initState = BC.BC_state(INITIAL, BC.WHITE)
        currS = initState
        prev_state = currS
        prev_move = None
        r = 0
        count = 0
        while end_time > time.time() and len(POLICY) < 1000000 and not hasLost(currS, side=BC.BLACK):
            if currS.whose_move == BC.BLACK:
                # currS = switchBlackAndWlhite(currS)
                valid_moves = Agent.available_moves(currS)
                if len(valid_moves) == 0:
                    break
                elif len(valid_moves) == 1:
                    best_move = valid_moves[0]
                else:
                    currS = switchBlackAndWlhite(currS)
                    if currS not in POLICY:
                        random_i = randint(0, len(valid_moves) - 1)
                        best_move = valid_moves[random_i]
                    else:
                        best_move = POLICY[currS]
                currS = Agent.move_piece(currS, best_move)
                currS = switchBlackAndWlhite(currS)
                continue

            moves = Agent.available_moves(currS)
            if len(moves) == 0: break
            max_val = getQVal((currS, moves[0]))
            POLICY[currS] = moves[0]
            for new_move in moves:
                temp = getQVal((currS, new_move))
                if(temp > max_val):
                    max_val = temp
                    POLICY[currS] = new_move

            sample = r + GAMMA * max_val
            new_qval = (1 - ALPHA)*getQVal((prev_state, prev_move))\
                       + ALPHA*sample

            # Save it in the dictionary of Q_VALUES:
            Q_VALUES[(prev_state, prev_move)] = new_qval

            chosen_action = None
            if random() > EPSILON and currS in POLICY:
                chosen_action = POLICY[currS]
            else:
                random_i = randint(0, len(moves) - 1)
                chosen_action = moves[random_i]

            prev_move = chosen_action
            prev_state = currS
            r = staticEval(currS)
            currS = Agent.move_piece(currS, chosen_action)
            count += 1
            if count % 300 == 0:
                print(str(count))
        print("Iteration "+str(n)+" completed")
        n += 1
    saveInfo()


def getQVal(tup):
    global Q_VALUES
    if tup in Q_VALUES:
        return Q_VALUES[tup]
    return 0

def switchBlackAndWlhite(state):
    opposite = 1 - state.whose_move
    newBoard = state.board[:][:]
    for i, row in enumerate(state.board):
        for j, piece in enumerate(row):
            if piece != 0:
                if piece % 2 == 0:
                    newBoard[i][j] = piece + 1
                else:
                    newBoard[i][j] = piece - 1
    return BC.BC_state(newBoard, opposite)

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
    '''
    # Learning took me a LONG time. Do not Learn unless you know you have a plenty of time
    start_time = time.time()
    learn(4 * 60 * 60 + 4 * 60) # 4 hours 40 minutes 4 * 60 * 60 + 40 * 60
    end_time = time.time()
    duration = end_time - start_time
    print("Duration: "+ str(duration))
    print("start_time: "+ str(start_time))
    print("end_time: "+ str(end_time))
    '''
