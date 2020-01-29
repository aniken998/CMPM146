from random import choice

def think(board, state):
    """ Returns a random move. """
    # print(board.unpack_state(state))
    return choice(board.legal_actions(state))
