from basic import *


def move_generate(game_board):
    move_list = []
    if game_board.min_row - 1 < 0:
        min_row = 0
    else:
        min_row = game_board.min_row
    if game_board.max_row + 2 > 15:
        max_row = 15
    else:
        max_row = game_board.max_row + 2
    if game_board.min_col - 1 < 0:
        min_col = 0
    else:
        min_col = game_board.min_col
    if game_board.max_col + 2 > 15:
        max_col = 15
    else:
        max_col = game_board.max_col + 2
    for row_index in range(min_row, max_row):
        for col_index in range(min_col, max_col):
            if game_board.board[row_index][col_index] != NO_CHESS:
                for r in range(row_index - 2, row_index + 3):
                    for c in range(col_index - 2, col_index + 3):
                        if 0 <= r < 15 and 0 <= c < 15:
                            if game_board.board[r][c] == NO_CHESS:
                                if [r, c] not in move_list:
                                    move_list.append([r, c])
    return move_list
