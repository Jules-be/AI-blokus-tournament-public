import copy


def adj_to(pos, array, char):
    return (pos[1] - 1 >= 0 and array[pos[1] - 1][pos[0]] == char) or (
                pos[1] + 1 < len(array) and array[pos[1] + 1][pos[0]] == char) or (
                                                  pos[0] + 1 < len(array[pos[1]]) and array[pos[1]][
                                              pos[0] + 1] == char) or (
                                                  pos[0] - 1 >= 0 and array[pos[1]][pos[0] - 1] == char)


def diag_to(pos, array, char):
    return (pos[0] - 1 >= 0 and pos[1] - 1 >= 0 and array[pos[1] - 1][
    pos[0] - 1] == char) or (pos[0] - 1 >= 0 and pos[1] + 1 < len(array) and array[pos[1] + 1][
                                       pos[0] - 1] == char) or (pos[0] + 1 < len(array[pos[1]]) and pos[
                                       1] - 1 >= 0 and array[pos[1] - 1][pos[0] + 1] == char) or (pos[
                                       0] + 1 < len(array[pos[1]]) and pos[1] + 1 < len(array) and
                                   array[pos[1] + 1][
                                       pos[0] + 1] == char)


class Piece:
    def __init__(self, self_id, player):
        self.id = self_id
        self.player = player
        self.pos = (-1, -1)
        self.shape = [['O' for __ in range(5)] for _ in range(5)]
        self.rotation = 0
        self.size = 0
        file = open("./resources/" + str(self.id) + ".txt")
        lines = file.readlines()
        for i in range(0, len(lines)):
            lines[i] = lines[i].strip('\n')
            for j in range(0, len(lines[i])):
                self.shape[i][j] = lines[i][j]
                if lines[i][j] == 'X':
                    self.size += 1

    def rotate_left(self):
        shape = copy.deepcopy(self.shape)

        self.rotation -= 90
        self.rotation %= 360
        for i in range(0, len(shape)):
            for j in range(0, len(shape[i])):
                self.shape[i][j] = shape[j][4 - i]

    def rotate_right(self):
        shape = copy.deepcopy(self.shape)

        self.rotation += 90
        self.rotation %= 360
        for i in range(0, len(shape)):
            for j in range(0, len(shape[i])):
                self.shape[i][4 - j] = shape[j][i]

    def can_be_placed(self, board, position, mandatory_pos):
        mandatory = False if mandatory_pos else True
        corner = False

        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] == 'O':
                    continue
                coord = (position[0] + x - 2, position[1] + y - 2)
                if coord[1] < 0 or coord[1] >= len(board) or coord[0] < 0 or coord[0] >= len(board[coord[1]]):
                    return False
                if board[coord[1]][coord[0]] != 'O':
                    return False
                if mandatory_pos and mandatory_pos[0] == coord[0] and mandatory_pos[1] == coord[1]:
                    mandatory = True
                if self.adjacent_part(board, coord):
                    return False
                corner = corner if corner else self.diagonal_part(board, coord)
        if not mandatory:
            return False
        if not corner and not mandatory_pos:
            return False
        return True

    def place(self, board, position):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] == 'O':
                    continue
                coord = (position[0] + x - 2, position[1] + y - 2)
                board[coord[1]][coord[0]] = chr(self.player + 48)
        self.pos = position

    def adjacent_part(self, board, coord):
        return adj_to(coord, board, chr(self.player + 48))

    def diagonal_part(self, board, coord):
        return diag_to(coord, board, chr(self.player + 48))

    def get_score(self):
        score = 0
        for line in self.shape:
            for char in line:
                if char == 'X':
                    score -= 1
        return score

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.shape])
