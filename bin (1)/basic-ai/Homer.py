#!/usr/bin/env python
import os
import random
import sys
from blokus_classes.piece import *


COMMAND = 0
ARG = 1

board = []
player_nb = -1

mandatory_pos = []

pieces_id = None
pieces = None


def start(size):
    global board, mandatory_pos

    width = int(size)

    if width != 14 and width != 20:
        exit(84)
    board = [['O' for _ in range(width)] for __ in range(width)]
    mandatory_pos = [(4, 4), (9, 9)] if width == 14 else [(0, 0), (19, 0), (0, 19), (19, 19)]
    pass


def player(player_id):
    global board, player_nb

    player_nb = int(player_id)
    if player_nb < 0 or player_nb > (1 if len(board) == 14 else 3):
        exit(84)
    pass


def play():
    global board, player_nb, mandatory_pos, pieces_id, pieces

    if not pieces_id:
        pieces_id = []
        send_msg("PIECES")
        order = sys.stdin.readline().strip('\n')
        print("CLIENT {}: RECEIVE: {}".format(os.getpid(), order), file=sys.stderr)
        while order != "DONE":
            pieces_id.append(int(order))
            order = sys.stdin.readline().strip('\n')
            print("CLIENT {}: RECEIVE: {}".format(os.getpid(), order), file=sys.stderr)
        pieces = [Piece(pieces_id[i], player_nb) for i in range(len(pieces_id))]

    for i in range(len(pieces) - 1, -1, -1):
        piece = pieces[i]
        for j in range(4):
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if piece.can_be_placed(copy.deepcopy(board), (x, y),
                                           mandatory_pos[player_nb] if len(pieces) == 21 else None):
                        send_msg("PLAY {0} {1} {2} {3}".format(piece.id, x, y, piece.rotation))
                        piece.place(board, (x, y))
                        order = sys.stdin.readline().strip('\n')
                        if order != "DONE":
                            exit(84)
                        else:
                            pieces_id.pop(i)
                            pieces.pop(i)
                            return
            piece.rotate_right()
    send_msg("SURRENDER")
    order = sys.stdin.readline().strip('\n')
    if order != "DONE":
        exit(84)
    else:
        pass


def played(player_id, piece_id, x, y, rotation):
    global board, player_nb

    player_id = int(player_id)
    piece_id = int(piece_id)
    x = int(x)
    y = int(y)
    rotation = int(rotation)
    if player_id < 0 or player_id > (1 if len(board) == 14 else 3) or player_id == player_nb:
        exit(84)
    if piece_id < 1 or piece_id > 21:
        exit(84)
    if x < 0 or x > len(board) - 1:
        exit(84)
    if y < 0 or y > len(board) - 1:
        exit(84)
    if rotation != 0 and rotation != 90 and rotation != 180 and rotation != 270:
        exit(84)

    piece = Piece(piece_id, player_id)

    if rotation == 90:
        piece.rotate_right()
    elif rotation == 180:
        piece.rotate_right()
        piece.rotate_right()
    elif rotation == 270:
        piece.rotate_left()

    piece.place(board, (x, y))
    pass


def send_msg(string):
    print(string)
    print("CLIENT {}: SEND: {}".format(os.getpid(), string), file=sys.stderr)
    sys.stdout.flush()


def get_line():
    line = sys.stdin.readline()
    print("CLIENT {}: RECEIVE: {}".format(os.getpid(), line), file=sys.stderr)
    return line.strip().split()


def main():
    commands = {
        "START": start,
        "PLAYER": player,
        "PLAY": play,
        "PLAYED": played,
    }

    while True:
        order = get_line()
        cmd_len = len(order)
        if cmd_len >= 2:
            commands[order[COMMAND]](*order[ARG:])
        elif cmd_len == 1:
            commands[order[COMMAND]]()
        else:
            print("EXITED {}".format(os.getpid()), file=sys.stderr)
            exit(0)


if __name__ == "__main__":
    main()
