from basic import *
import numpy as np


class GameBoard:

    def __init__(self):
        self.board = np.zeros([15, 15])
        self.history = []
        self.min_row = None
        self.max_row = None
        self.min_col = None
        self.max_col = None

    def make_move(self, move, side):
        self.history.append(move)
        self.board[move[0]][move[1]] = side
        if self.min_row is None:
            self.min_row = move[0]
            self.max_row = move[0]
            self.min_col = move[1]
            self.max_col = move[1]
        else:
            if move[0] < self.min_row:
                self.min_row = move[0]
            elif move[0] > self.max_row:
                self.max_row = move[0]
            if move[1] < self.min_col:
                self.min_col = move[1]
            elif move[1] > self.max_col:
                self.max_col = move[1]

    def judge(self):
        if self.min_row is None:
            return None
        for row_index in range(self.min_row, self.max_row+1):
            for col_index in range(self.min_col, self.max_col+1):
                #横向检查
                if self.board[row_index][col_index] != NO_CHESS:
                    side = self.board[row_index][col_index]
                    count = 1
                    r = row_index-1
                    while 0<=r<15:
                        if self.board[r][col_index] == side:
                            count +=1
                            r -= 1
                        else:
                            break
                    r = row_index + 1
                    while 0 <= r < 15:
                        if self.board[r][col_index] == side:
                            count += 1
                            r += 1
                        else:
                            break
                    if count >= 5:
                        return side
                    #竖向检查
                    count = 1
                    c = col_index - 1
                    while 0 <= r < 15:
                        if self.board[row_index][c] == side:
                            count += 1
                            c -= 1
                        else:
                            break
                    c = col_index + 1
                    while 0 <= c < 15:
                        if self.board[row_index][c] == side:
                            count += 1
                            c += 1
                        else:
                            break
                    if count >= 5:
                        return side
                    #斜向检查
                    count = 1
                    r = row_index - 1
                    c = col_index - 1
                    while 0 <= r < 15 and 0 <= c < 15:
                        if self.board[r][c] == side:
                            count += 1
                            c -= 1
                            r -= 1
                        else:
                            break
                    r = row_index + 1
                    c = col_index + 1
                    while 0 <= r < 15 and 0 <= c < 15:
                        if self.board[r][c] == side:
                            count += 1
                            c += 1
                            r += 1
                        else:
                            break
                    if count >= 5:
                        return side
                    #斜向检查
                    count = 1
                    r = row_index - 1
                    c = col_index + 1
                    while 0 <= r < 15 and 0 <= c < 15:
                        if self.board[r][c] == side:
                            count += 1
                            c += 1
                            r -= 1
                        else:
                            break
                    r = row_index + 1
                    c = col_index - 1
                    while 0 <= r < 15 and 0 <= c < 15:
                        if self.board[r][c] == side:
                            count += 1
                            c -= 1
                            r += 1
                        else:
                            break
                    if count >= 5:
                        return side
        return None
