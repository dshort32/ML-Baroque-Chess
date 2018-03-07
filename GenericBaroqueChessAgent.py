'''GenericBaroqueChessAgent.py

Basic template for any agent. Describes movements, constraints, and capturing.
Contains tests for making sure the pieces are moving and capturing in the
Correct manner.
'''

import BC_state_etc as BC

def move_piece(currentState, move, capture_mode=True):
    # Capture_mode is for when wanting to make moves without
    # capturing or turning the game over to the opponent
    turn = currentState.whose_move
    next_state = BC.BC_state(currentState.board, turn)
    if capture_mode:
        next_state.whose_move = 1 - currentState.whose_move

    start, end = move
    piece = next_state.board[start[0]][start[1]]
    next_state.board[start[0]][start[1]] = 0
    next_state.board[end[0]][end[1]] = piece
    if capture_mode:
        removed_pieces = remove_captured(next_state, move)
    return next_state

def remove_captured(state_to_update, move):
    board = state_to_update.board
    start, end = move
    moved_piece = board[end[0]][end[1]]
    player = BC.who(moved_piece)
    opponent = 1 - player
    removed_pieces = []
    if moved_piece == BC.BLACK_WITHDRAWER or moved_piece == BC.WHITE_WITHDRAWER\
        or moved_piece == BC.BLACK_IMITATOR or moved_piece == BC.WHITE_IMITATOR:
        delta_i = end[0] - start[0]
        delta_j = end[1] - start[1]
        target_i = start[0] if delta_i == 0 else start[0] - int((delta_i) / abs(delta_i))
        target_j = start[1] if delta_j == 0 else start[1] - int((delta_j) / abs(delta_j))
        removed_location = target_i, target_j

        # Either Withdrawer or Imitator can remove pieces by Withdrawing
        if inbounds(state_to_update, removed_location)\
            and BC.who(board[target_i][target_j]) == opponent\
            and board[target_i][target_j] != 0\
            and (moved_piece == BC.BLACK_WITHDRAWER or moved_piece == BC.WHITE_WITHDRAWER\
                or (moved_piece == BC.BLACK_IMITATOR and board[target_i][target_j] == BC.WHITE_WITHDRAWER)
                or (moved_piece == BC.WHITE_IMITATOR and board[target_i][target_j] == BC.BLACK_WITHDRAWER)):
            removed_piece = board[target_i][target_j]
            board[target_i][target_j] = 0
            removed_pieces.append((removed_piece, removed_location))
    if moved_piece == BC.BLACK_PINCER or moved_piece == BC.WHITE_PINCER\
        or moved_piece == BC.BLACK_IMITATOR or moved_piece == BC.WHITE_IMITATOR:

        # Pincer can only remove pieces in the four cardinal directions, instad of all eight
        for pos in [(1,0),(-1,0),(0,1),(0,-1)]:
            target_i = end[0] + pos[0]
            target_j = end[1] + pos[1]
            pos_across= end[0] + 2 * pos[0], end[1] + 2 * pos[1]
            removed_location = target_i, target_j
            # print("pos_across: "+str(pos_across) +" pos: "+str(end[0] + 2 * pos[0]))

            # Either Pincer or Imitator can remove by sanwiching opponet's pieces
            if inbounds(state_to_update, removed_location)\
                and inbounds(state_to_update, pos_across)\
                and BC.who(board[target_i][target_j]) == opponent\
                and board[target_i][target_j] != 0\
                and BC.who(board[pos_across[0]][pos_across[1]]) == player\
                and board[pos_across[0]][pos_across[1]] != 0\
                and (moved_piece == BC.BLACK_PINCER or moved_piece == BC.WHITE_PINCER\
                    or (moved_piece == BC.BLACK_IMITATOR and board[target_i][target_j] == BC.WHITE_PINCER)
                    or (moved_piece == BC.WHITE_IMITATOR and board[target_i][target_j] == BC.BLACK_PINCER)):
                removed_piece = board[target_i][target_j]
                board[target_i][target_j] = 0
                removed_pieces.append((removed_piece, removed_location))
    if moved_piece == BC.BLACK_COORDINATOR or moved_piece == BC.WHITE_COORDINATOR\
        or moved_piece == BC.BLACK_IMITATOR or moved_piece == BC.WHITE_IMITATOR:
        kingPos = (0, 0)

        # Find the King's Position
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if (piece == BC.BLACK_KING or piece == BC.WHITE_KING)\
                    and BC.who(piece) == player:
                    kingPos = (i,j)
                    break;

        # Either Coordinator or Imitator can coordinate remove a piece
        for target_pos in [(end[0], kingPos[1]), (kingPos[0], end[1])]:
            potential_captured_piece = board[target_pos[0]][target_pos[1]]
            if BC.who(potential_captured_piece) == opponent and potential_captured_piece != 0\
                and (moved_piece == BC.BLACK_COORDINATOR or moved_piece == BC.WHITE_COORDINATOR\
                    or (moved_piece == BC.BLACK_IMITATOR and board[target_pos[0]][target_pos[1]] == BC.WHITE_COORDINATOR)
                    or (moved_piece == BC.WHITE_IMITATOR and board[target_pos[0]][target_pos[1]] == BC.BLACK_COORDINATOR)):
                board[target_pos[0]][target_pos[1]] = 0
                removed_pieces.append((potential_captured_piece, target_pos))

    if moved_piece == BC.BLACK_LEAPER or moved_piece == BC.WHITE_LEAPER\
        or moved_piece == BC.BLACK_IMITATOR or moved_piece == BC.WHITE_IMITATOR:
        delta_i = end[0] - start[0]
        delta_j = end[1] - start[1]
        target_i = end[0] if delta_i == 0 else end[0] - int((delta_i) / abs(delta_i))
        target_j = end[1] if delta_j == 0 else end[1] - int((delta_j) / abs(delta_j))
        removed_location = target_i, target_j

        # Either Leaper or Imitator can leap
        if inbounds(state_to_update, removed_location)\
            and BC.who(board[target_i][target_j]) == opponent\
            and board[target_i][target_j] != 0\
            and (moved_piece == BC.BLACK_LEAPER or moved_piece == BC.WHITE_LEAPER\
                or (moved_piece == BC.BLACK_IMITATOR and board[target_i][target_j] == BC.WHITE_LEAPER)
                or (moved_piece == BC.WHITE_IMITATOR and board[target_i][target_j] == BC.BLACK_LEAPER)):
            removed_piece = board[target_i][target_j]
            board[target_i][target_j] = 0
            removed_pieces.append((removed_piece, removed_location))

    return removed_pieces

def available_moves(currentState):
    # Copy the state and the board
    turn = currentState.whose_move
    initialStateCopied = BC.BC_state(currentState.board, turn)
    board = initialStateCopied.board
    available_move_list = []
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            currPos = (i,j)

            # If not your piece or frozen, don't do anything
            if (BC.who(piece) == BC.BLACK and turn == BC.WHITE)\
                or (BC.who(piece) == BC.WHITE and turn == BC.BLACK)\
                or isFrozen(initialStateCopied, currPos) or (piece == 0):
                continue

            # Adding King's moves
            if piece == BC.BLACK_KING or piece == BC.WHITE_KING:
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

def order(state, moves_list):
    dictionary = {}
    for move in moves_list:
        newState = move_piece(state, move)
        hashed = getStateHash(newState)
        dictionary[len(available_moves(newState))] = move
    newList = []
    mobility = sorted(dictionary.keys())
    for m  in mobility:
        newList.append(dictionary[m])
    return newList


def getStateHash(state):
    return (str(state)).__hash__()


def isFrozen(state, position):
    opponent = 1 - state.whose_move
    for i_k in range(-1, 2) :
        for j_k in range(-1, 2) :
            i, j = position[0] + i_k, position[1] + j_k
            if not inbounds(state, (i, j)) or position == (i, j):
                continue
            currentPiece = state.board[position[0]][position[1]]
            adjacent_piece = state.board[i][j]

            # Either Freezer or an Imitator can Freeze a piece
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

def recursive_find_moves(currState, startPos, currPos, delta_i, delta_j, available_move_list):
    board = currState.board
    curRow, curCol = currPos
    newPosition = curRow + delta_i, curCol + delta_j
    curPiece = board[curRow][curCol]

    # Recurse another time if there is more room to explore
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


t0 = (BC.parse('''
- - - - - - - -
- - - - - - p p
- - - - - - - i
- - - - - - - -
- - - k - - - -
- - - W - - - -
- - - - L K - -
- - - - - - - -
'''), 1, "Capture : Withdrawer", ((2,6),(5,3)))

t1 = (BC.parse('''
- - - - - - - -
- - - k - - - -
- - - P - C - -
- - - p w - - -
- K f P - - - -
- - - i - - l -
- - - - - - P -
- - - W - - - -
'''), 2, "Capture : Pincer", ((4,6),(4,3)))

t2 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - l - i C - -
- - - - - - k -
- - - - - - - -
- - - - - P - -
- - K p - f - -
- - - - - - - -
'''), 2, "Capture : Coordinator", ((4,3),(2,5)))

t3 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - p - - - -
- - L - - - - -
- - - - - - - -
'''), 1, "Capture : Leaper", ((4,4),(6,2)))

t4 = (BC.parse('''
- - - - - - - -
- - - - - - p w
- - - - - - - i
- - - - - - - -
- - - k - - - -
- - - I - - - -
- - - - L K - -
- - - - - - - -
'''), 1, "Capture : Imitator1", ((2,6), (5,3)))

t5 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - I p P c -
- - - - - - - -
- - - - - - - -
w - - c - - K -
'''), 4, "Capture : Imitator2", ((6,1),(4,3)))

t11 = (BC.parse('''
- - - - - - - -
- - - k - - - -
- - - P - C - -
- - - p w - - -
- K p I - - - -
- - - p - - l -
- - - W - - P -
- - - - - - - -
'''), 3, "Capture : Imitator3", ((4,6),(4,3)))

t12 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - c - p I - -
- - - - - - k -
- - - - - - - -
- - - - - P - -
- - K p - f - -
- - - - - - - -
'''), 1, "Capture : Imitator4", ((4,3),(2,5)))

def basic_capture_test():
    # Witherdrawer
    currentState = BC.BC_state(t0[0], BC.WHITE)
    captured = remove_captured(currentState, t0[3])
    check(t0, len(captured))

    # Pincer
    currentState = BC.BC_state(t1[0], BC.WHITE)
    captured = remove_captured(currentState, t1[3])
    check(t1, len(captured))

    # Coordinator
    currentState = BC.BC_state(t2[0], BC.WHITE)
    captured = remove_captured(currentState, t2[3])
    check(t2, len(captured))

    # Leaper
    currentState = BC.BC_state(t3[0], BC.WHITE)
    captured = remove_captured(currentState, t3[3])
    check(t3, len(captured))

    # Imitator1
    currentState = BC.BC_state(t4[0], BC.WHITE)
    captured = remove_captured(currentState, t4[3])
    check(t4, len(captured))

    # Imitator2
    currentState = BC.BC_state(t5[0], BC.WHITE)
    captured = remove_captured(currentState, t5[3])
    check(t5, len(captured))

    # Imitator3
    currentState = BC.BC_state(t11[0], BC.WHITE)
    captured = remove_captured(currentState, t11[3])
    check(t11, len(captured))

    # Imitator4
    currentState = BC.BC_state(t12[0], BC.WHITE)
    captured = remove_captured(currentState, t12[3])
    check(t12, len(captured))

t6 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - p - - - -
p - p - - - - -
p - - - - - - -
L - - - - p - -
'''), 6, "Movement: Leaper")

t7 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - K - - - -
- - - - - - - -
- - - - - - - -
'''), 8, "Movement: King")

t8 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- f - - - - - -
W - - - - - - -
'''), 0, "Movement: Freezer")

t9 = (BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- i - - - - - -
F - - - - - - -
'''), 0, "Movement: Imitator")

t10 = (BC.parse('''
- - - p - - - -
p - - - - - - -
- - - - - - - -
- - - - - - - -
- p - W - - - -
- - - - - - - -
- - - - - - - -
p - - - - - - -
'''), 22, "Movement: Withdrawer")

# Helper method. Same funcationality as the "assert" statement
def check(test, actual_val):
    if test[1] == actual_val:
        print(test[2]+" - success")
    else:
        print(test[2]+" - FAIL found: "+ str(actual_val)+" should be: "+str(test[1]))

def basic_movement_test():
    # Leaper
    currentState = BC.BC_state(t6[0], BC.WHITE)
    moves = available_moves(currentState)
    check(t6, len(moves))

    # King
    currentState = BC.BC_state(t7[0], BC.WHITE)
    moves = available_moves(currentState)
    check(t7, len(moves))

    # Freezer
    currentState = BC.BC_state(t8[0], BC.WHITE)
    moves = available_moves(currentState)
    check(t8, len(moves))

    # Imitator
    currentState = BC.BC_state(t9[0], BC.WHITE)
    moves = available_moves(currentState)
    check(t9, len(moves))

    # Withdrawer
    currentState = BC.BC_state(t10[0], BC.WHITE)
    moves = available_moves(currentState)
    check(t10, len(moves))

if __name__ == '__main__':
   basic_capture_test()
   basic_movement_test()
