from basic import *
import numpy as np


def evaluate(game_board, side):
    return evaluate_side(game_board, side) - evaluate_side(game_board, -side)


def evaluate_side(game_board, side):
    x = 0
    for row_index in range(game_board.min_row, game_board.max_row + 1):
        for col_index in range(game_board.min_col, game_board.max_col + 1):
            if game_board.board[row_index][col_index] == side:
                counts = connect_num(game_board.board, row_index, col_index)
                value = np.zeros(9)

                for axis in range(len(counts)):
                    if counts[axis] == 5:
                        return 100000
                    elif counts[axis] == 4:
                        up_1 = look_forward(game_board.board, row_index, col_index, 1, axis)
                        re_up_1 = look_forward(game_board.board, row_index, col_index, -1, axis)
                        if up_1 == NO_CHESS or re_up_1 == NO_CHESS:
                            value[8] += 1
                            continue  # 活4
                        elif up_1 + re_up_1 == -side:
                            value[0] += 1  # 死4
                            continue
                    elif counts[axis] == 3:
                        up_1 = look_forward(game_board.board, row_index, col_index, 1, axis)
                        re_up_1 = look_forward(game_board.board, row_index, col_index, -1, axis)
                        up_2 = look_forward(game_board.board, row_index, col_index, 2, axis)
                        re_up_2 = look_forward(game_board.board, row_index, col_index, -2, axis)
                        if up_1 == NO_CHESS and re_up_1 == NO_CHESS:
                            if up_2 == -side and re_up_2 == -side:
                                value[3] += 1  # 死3
                                continue
                            elif up_2 == side or re_up_2 == side:
                                value[1] += 1  # 低级死4
                                continue
                            elif up_2 == NO_CHESS or re_up_2 == NO_CHESS:
                                value[2] += 1  # 活3
                                continue
                        elif up_1 == NO_CHESS or re_up_1 == NO_CHESS:
                            if up_1 == -side:  # 左边被对方堵住
                                if re_up_2 == NO_CHESS:  # 右边均空
                                    value[3] += 1
                                    continue
                                elif re_up_2 == side:
                                    value[1] += 1
                                    continue
                            elif re_up_1 == -side:  # 右边被对方堵住
                                if up_2 == NO_CHESS:  # 左边均空
                                    value[3] += 1
                                    continue
                                elif up_2 == side:  # 左边还有自己的棋子
                                    value[1] += 1
                                    continue

                    elif counts[axis] == 2:
                        up_1 = look_forward(game_board.board, row_index, col_index, 1, axis)
                        re_up_1 = look_forward(game_board.board, row_index, col_index, -1, axis)
                        up_2 = look_forward(game_board.board, row_index, col_index, 2, axis)
                        re_up_2 = look_forward(game_board.board, row_index, col_index, -2, axis)
                        up_3 = look_forward(game_board.board, row_index, col_index, 3, axis)
                        re_up_3 = look_forward(game_board.board, row_index, col_index, -3, axis)
                        if up_1 == NO_CHESS and re_up_1 == NO_CHESS:  # 两边断开位置均空
                            if (re_up_2 == NO_CHESS and re_up_3 == side) or (up_2 == NO_CHESS and up_3 == side):
                                value[3] += 1  # 死3
                                continue
                            elif up_2 == NO_CHESS and re_up_2 == NO_CHESS:
                                value[5] += 1  # 活2
                                continue
                            elif (re_up_2 == side and re_up_3 == -side) or (up_2 == side and up_3 == -side):
                                value[3] += 1  # 死3
                                continue
                            elif (re_up_2 == side and re_up_3 == side) or (up_2 == side and up_3 == side):
                                value[1] += 1  # 死4
                                continue
                            elif (re_up_2 == side and re_up_3 == NO_CHESS) or (up_2 == side and up_3 == NO_CHESS):
                                value[4] += 1  # 跳活3
                                continue
                            # 其他情况在下边返回NOTHREAT

                        elif up_1 == NO_CHESS or re_up_1 == NO_CHESS:  # 两边断开位置只有一个空
                            if up_1 == -side:  # 左边被对方堵住
                                if re_up_2 == NO_CHESS and re_up_3 == NO_CHESS:  # 均空
                                    value[7] += 1  # 死2
                                    continue
                                elif re_up_2 == side and re_up_3 == side:  # 均为自己的棋子
                                    value[1] += 1  # 死4
                                    continue
                                elif re_up_2 == side or re_up_3 == side:  # 只有一个自己的棋子
                                    value[3] += 1  # 死3
                                    continue
                            elif re_up_1 == -side:  # 右边被对方堵住
                                if up_2 == NO_CHESS and up_3 == NO_CHESS:  # 均空
                                    value[7] += 1  # 死2
                                    continue
                                elif up_2 == side and up_3 == side:  # 均为自己的棋子
                                    value[1] += 1  # 死4
                                    continue
                                elif up_2 == side or up_3 == side:  # 只有一个自己的棋子
                                    value[3] += 1  # 死3
                                    continue

                    elif counts[axis] == 1:
                        up_1 = look_forward(game_board.board, row_index, col_index, 1, axis)
                        re_up_1 = look_forward(game_board.board, row_index, col_index, -1, axis)
                        up_2 = look_forward(game_board.board, row_index, col_index, 2, axis)
                        re_up_2 = look_forward(game_board.board, row_index, col_index, -2, axis)
                        up_3 = look_forward(game_board.board, row_index, col_index, 3, axis)
                        re_up_3 = look_forward(game_board.board, row_index, col_index, -3, axis)
                        up_4 = look_forward(game_board.board, row_index, col_index, 4, axis)
                        re_up_4 = look_forward(game_board.board, row_index, col_index, -4, axis)
                        if up_1 == NO_CHESS and up_2 == side and up_3 == side and up_4 == side:
                            value[1] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == side and re_up_3 == side and re_up_4 == side:
                            value[1] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == side and up_3 == side and up_4 == NO_CHESS and re_up_1 == NO_CHESS:
                            value[4] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == side and re_up_3 == side and re_up_4 == NO_CHESS and up_1 == NO_CHESS:
                            value[4] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == side and up_3 == side and up_4 == -side and re_up_1 == NO_CHESS:
                            value[3] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == side and re_up_3 == side and re_up_4 == -side and up_1 == NO_CHESS:
                            value[3] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == NO_CHESS and up_3 == side and up_4 == side:
                            value[3] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == NO_CHESS and re_up_3 == side and re_up_4 == side:
                            value[3] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == side and up_3 == NO_CHESS and up_4 == side:
                            value[3] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == side and re_up_3 == NO_CHESS and re_up_4 == side:
                            value[3] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == side and up_3 == NO_CHESS and up_4 == NO_CHESS and re_up_1 == NO_CHESS:
                            value[6] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == side and re_up_3 == NO_CHESS and re_up_4 == NO_CHESS and up_1 == NO_CHESS:
                            value[6] += 1
                            continue
                        elif up_1 == NO_CHESS and up_2 == NO_CHESS and up_3 == side and up_4 == NO_CHESS and re_up_1 == NO_CHESS:
                            value[6] += 1
                            continue
                        elif re_up_1 == NO_CHESS and re_up_2 == NO_CHESS and re_up_3 == side and re_up_4 == NO_CHESS and up_1 == NO_CHESS:
                            value[6] += 1
                            continue

                if value[0] >= 2 or (value[0] and value[2]) or value[8]:
                    x += 10000
                if value[2] >= 2:
                    x += 5000
                if value[2] and value[3]:
                    x += 1000
                if value[0]:
                    x += 500
                if value[1]:
                    x += 400
                if value[2] == 1:
                    x += 100
                if value[4]:
                    x += 90
                if value[5] >= 2:
                    x += 50
                elif value[5]:
                    x += 10
                if value[6]:
                    x += 9
                if value[3]:
                    x += 5
                if value[7]:
                    x += 2
                else:
                    x += 1
    return x


def look_forward(board, x, y, step, axis):
    count = 0
    side = board[x][y]
    if step > 0:
        sp = 1
    elif step < 0:
        sp = -1
    if axis == 0:
        while 0 <= x + sp < 15:
            x += sp
            if board[x][y] != side:
                count += 1
            if count == step:
                return board[x][y]
    elif axis == 1:
        while 0 <= y + sp < 15:
            y += sp
            if board[x][y] != side:
                count += 1
            if count == step:
                return board[x][y]
    elif axis == 2:
        while 0 <= x + sp < 15 and 0 <= y + sp < 15:
            x += sp
            y += sp
            if board[x][y] != side:
                count += 1
            if count == step:
                return board[x][y]
    elif axis == 3:
        while 0 <= x + sp < 15 and 0 <= y - sp < 15:
            x += sp
            y -= sp
            if board[x][y] != side:
                count += 1
            if count == step:
                return board[x][y]
    return -side


def connect_num(board, x, y):
    # 横向检查
    count = [1, 1, 1, 1]
    side = board[x][y]
    r = x - 1
    while 0 <= r < 15:
        if board[r][y] == side:
            count[0] += 1
            r -= 1
        else:
            break
    r = x + 1
    while 0 <= r < 15:
        if board[r][y] == side:
            count[0] += 1
            r += 1
        else:
            break

    # 竖向检查
    c = y - 1
    while 0 <= r < 15:
        if board[x][c] == side:
            count[1] += 1
            c -= 1
        else:
            break
    c = y + 1
    while 0 <= c < 15:
        if board[x][c] == side:
            count[1] += 1
            c += 1
        else:
            break
    # 斜向检查
    r = x - 1
    c = y - 1
    while 0 <= r < 15 and 0 <= c < 15:
        if board[r][c] == side:
            count[2] += 1
            c -= 1
            r -= 1
        else:
            break
    r = x + 1
    c = y + 1
    while 0 <= r < 15 and 0 <= c < 15:
        if board[r][c] == side:
            count[2] += 1
            c += 1
            r += 1
        else:
            break

    # 斜向检查
    r = x - 1
    c = y + 1
    while 0 <= r < 15 and 0 <= c < 15:
        if board[r][c] == side:
            count[3] += 1
            c += 1
            r -= 1
        else:
            break
    r = x + 1
    c = y - 1
    while 0 <= r < 15 and 0 <= c < 15:
        if board[r][c] == side:
            count[3] += 1
            c -= 1
            r += 1
        else:
            break

    return count
