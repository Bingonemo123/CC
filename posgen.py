import chess
import numpy as np


def psgenesis(prob=0.5):
    board = chess.Board()
    gameflow = []
    while not board.is_game_over():
        move = np.random.choice(list(board.legal_moves))
        board.push(move)
        gameflow.append(board.copy())

    if np.random.choice([True, False],p=[prob, 1-prob]):
        return board

    else:
        ch = np.random.choice(gameflow)
        return ch



def map(rb):
    k = []
    for x in range(64):
        if x in rb.piece_map():
            tp = rb.piece_map()[x].piece_type
            cl = rb.piece_map()[x].color
            k.append(float((-1)**(cl == chess.BLACK) * tp))
        else:
            k.append(0.0)

    return k