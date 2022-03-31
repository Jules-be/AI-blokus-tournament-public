#!/usr/bin/env python3
import os
import sys
from blokus_classes.piece import *

COMMAND = 0
ARG = 1

board = []
player_nb = -1
turn = 0
startmoves = [[18, (-1, -1), 270], [20, (-1, -1), 0], [21, (-1, -1), 0], [15, (-1, -1), 180]]

bestpiece= [21, 20, 18, 19, 16, 15, 14, 12, 17, 13, 11, 10, 9, 7, 6, 8, 5, 4, 3, 2, 1]

mandatory_pos = []

pieces = []


def start(size):
    global board, mandatory_pos

    width = int(size)

    if width != 14 and width != 20:
        exit(84)
    board = [['O' for _ in range(width)] for __ in range(width)]
    mandatory_pos = [(4, 4), (9, 9)] if width == 14 else [(0, 0), (19, 0), (0, 19), (19, 19)]
    pass


def player(player_id):
    global board, player_nb, pieces, startmoves

    player_nb = int(player_id)
    if player_nb < 0 or player_nb > (1 if len(board) == 14 else 3):
        exit(84)
    pieces = []
    for i in range(1, 22):
        pieces.append(Piece(i, player_nb))
    pass


def prout(array, piece_size):
    global player_nb

    player_corners = 0
    opponent_corners = 0

    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] != 'O':
                continue
            for ply_id in range(0, (1 if len(array) == 14 else 3) + 1):
                corner = diag_to((j, i), array, chr(ply_id + 48)) and not adj_to((j, i), array, chr(ply_id + 48))
                if corner:
                    if ply_id == player_nb:
                        player_corners += 1
                    else:
                        opponent_corners += 1

    weight = piece_size * 2 + (player_corners - opponent_corners * 3)
    return weight


def play():
    global board, player_nb, mandatory_pos, pieces, turn, startmoves

    possible_positions = []
    p_i = None
    if turn <= 3 and len(board) == 20:
        for p in range(len(pieces)):
            if pieces[p].id == startmoves[turn][0]:
                p_i = p
                while pieces[p].rotation != startmoves[turn][2]:
                    pieces[p].rotate_right()

    possible_positions = []

    if turn <= 3 and len(board) == 20 and p_i and pieces[p_i].can_be_placed(copy.deepcopy(board),
                                                                            startmoves[turn][1],
                                                                            mandatory_pos[player_nb] if len(
                                                                                    pieces) == 21 else None):
        possible_positions.append((p_i, pieces[p_i].id, startmoves[turn][1], startmoves[turn][2], 100000000))
    else:
        for i in range(len(pieces) - 1, -1, -1):
            piece = pieces[i]
            for j in range(4):
                for y in range(len(board)):
                    for x in range(len(board[y])):
                        board_copy = copy.deepcopy(board)
                        if piece.can_be_placed(board_copy, (x, y),
                                               mandatory_pos[player_nb] if len(pieces) == 21 else None):
                            piece.place(board_copy, (x, y))
                            possible_positions.append(
                                (i, piece.id, (x, y), piece.rotation, prout(board_copy, piece.size)))
                piece.rotate_right()

    if len(possible_positions):
        dicksize = max(pos[4] for pos in possible_positions)
        possible_positions = list(filter(lambda elem: elem[4] == dicksize, possible_positions))
        
        i = possible_positions[0][0]
        piece = pieces[i]

        send_msg("PLAY {0} {1} {2} {3}".format(possible_positions[0][1], possible_positions[0][2][0],
                                               possible_positions[0][2][1], possible_positions[0][3]))
        while piece.rotation != possible_positions[0][3]:
            piece.rotate_right()
        piece.place(board, possible_positions[0][2])

        turn += 1
        order = sys.stdin.readline().strip('\n')
        if order != "DONE":
            exit(84)
        else:
            pieces.pop(i)
            return
    else:
        send_msg("SURRENDER")
        order = sys.stdin.readline().strip('\n')
        if order != "DONE":
            exit(84)
        else:
            return


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
