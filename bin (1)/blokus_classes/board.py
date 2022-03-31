from blokus_classes.piece import *


class Board:
    def __init__(self, player_nb):
        self.player_nb = player_nb
        if player_nb == 2:
            self.size = 14
            self.player_start_pos = [(4, 4), (9, 9)]
        elif player_nb == 4:
            self.size = 20
            self.player_start_pos = [(0, 0), (19, 0), (0, 19), (19, 19)]
        else:
            raise ValueError
        self.board = [['O' for __ in range(self.size)] for _ in range(self.size)]
        self.turn = 0
        self.player_pieces = [[Piece(i, p) for i in range(1, 22)] for p in range(self.player_nb)]
        self.board_pieces = []
        self.surrender = [False for _ in range(self.player_nb)]

    def next_turn(self):
        self.turn += 1
        self.turn %= self.player_nb
        while self.surrender[self.turn]:
            self.turn += 1
            self.turn %= self.player_nb

    def check_end(self):
        for s in self.surrender:
            if not s:
                return False
        return True

    def place_piece(self, player_id, piece_id, position):
        saved_piece = None
        saved_id = None

        if player_id != self.turn:
            raise ValueError("Class Board: Place Piece: Wrong turn")
        if piece_id < 1 or piece_id > 21:
            raise ValueError("Class Board: Place Piece: Wrong piece id")
        for piece in self.board_pieces:
            if piece.id == piece_id and piece.player == player_id:
                raise ValueError("Class Board: Place Piece: Piece already placed")
        first_move = len(self.player_pieces[self.turn]) == 21
        if len(self.player_pieces[self.turn]) == 0:
            self.surrender[self.turn] = True
            return
        for i in range(len(self.player_pieces[self.turn])):
            piece = self.player_pieces[self.turn][i]
            if piece_id != piece.id:
                continue
            if not piece.can_be_placed(copy.deepcopy(self.board), position,
                                       None if not first_move else self.player_start_pos[self.turn]):
                raise ValueError("Class Board: Place Piece: Can't place piece")
            piece.place(self.board, position)
            saved_id = i
            saved_piece = piece
        if saved_id is not None and saved_piece is not None:
            self.player_pieces[self.turn].pop(saved_id)
            self.board_pieces.append(saved_piece)

    def count_points(self, player_id):
        score = 0
        if player_id < 0 or player_id > self.player_nb - 1:
            raise ValueError
        if len(self.player_pieces[player_id]) == 0:
            score += 15
            for i in range(len(self.board_pieces) - 1, -1, -1):
                if self.board_pieces[i].player == player_id:
                    if self.board_pieces[i].id == 1:
                        score += 5
                    break
        else:
            for piece in self.player_pieces[player_id]:
                score += piece.get_score()
        return score

    def rotate_piece(self, player_id, piece_id, side):
        # if player_id != self.turn:
        # raise ValueError
        if piece_id < 1 or piece_id > 21:
            raise ValueError
        if side != "right" and side != "left":
            raise ValueError
        for piece in self.board_pieces:
            if piece.id == piece_id and piece.player == player_id:
                raise ValueError
        for piece in self.player_pieces[player_id]:
            if piece.id == piece_id:
                if side == "right":
                    piece.rotate_right()
                else:
                    piece.rotate_left()
                return

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.board]) + '\n'
