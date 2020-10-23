from basic import *
import numpy as np


class GameBoard:

    def __init__(self):
        self.board = np.zeros([15, 15])  # 生成空棋盘
        self.min_row = None  # 有棋子的最小行数
        self.max_row = None  # 有棋子的最大行数
        self.min_col = None  # 有棋子的最小列数
        self.max_col = None  # 有棋子的最大列数

    def make_move(self, move, side, history=None):
        self.board[move[0]][move[1]] = side  # 放置棋子
        if self.min_row is None:    # 维护行列范围记录
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
        if history is not None:  # 记录下棋历史序列
            history.append(move)

    def judge(self):    # 判断是否有一方胜利， None代表没有胜利，返回其他值代表相应的胜利方
        if self.min_row is None:    # 代表棋盘为空，直接返回
            return None
        for row_index in range(self.min_row, self.max_row + 1):  # 遍历所有有棋子的点
            for col_index in range(self.min_col, self.max_col + 1):
                # 横向检查
                if self.board[row_index][col_index] != NO_CHESS:    # 如果棋盘上有棋子
                    if self.count_direction(row_index, col_index, 1, 0) >= 5:   # 横向检查
                        return self.board[row_index][col_index]
                    if self.count_direction(row_index, col_index, 0, 1) >= 5:   # 竖向检查
                        return self.board[row_index][col_index]
                    if self.count_direction(row_index, col_index, 1, 1) >= 5:   # 斜向检查
                        return self.board[row_index][col_index]
                    if self.count_direction(row_index, col_index, 1, -1) >= 5:  # 斜向检查
                        return self.board[row_index][col_index]
        return None  # 没有赢家

    def count_direction(self, row, col, row_step, col_step):    # 根据方向，记录相联棋子数
        count = 1   # 初始化计数器
        r = row - row_step
        c = col - col_step
        while 0 <= r < 15 and 0 <= c < 15:
            if self.board[r][c] == self.board[row][col]:
                count += 1  # 计数器+1
                r -= row_step   # 根据方向移动
                c -= col_step
            else:
                break
        r = row + row_step
        c = col + col_step
        while 0 <= r < 15 and 0 <= c < 15:
            if self.board[r][c] == self.board[row][col]:
                count += 1
                r += row_step
                c += col_step
            else:
                break
        return count