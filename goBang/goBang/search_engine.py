import random
from copy import deepcopy
import math
from basic import *
from move_generator import move_generate
from evaluator import evaluate


def uct_select(node, mode):
    if mode == 1:
        try:
            max_uct = node.children[0].reward / node.children[0].travel_num + math.sqrt(
                2 * math.log(node.travel_num) / node.children[0].travel_num)
        except ZeroDivisionError:
            return node.children[0]
        index = 0
        for c_index in range(len(node.children)):
            try:
                uct = node.children[c_index].reward / node.children[c_index].travel_num + math.sqrt(
                    2 * math.log(node.travel_num) / node.children[c_index].travel_num)
            except ValueError:
                uct = 0
            except ZeroDivisionError:
                return node.children[c_index]
            if uct > max_uct:
                max_uct = uct
                index = c_index
        return node.children[index]
    else:
        try:
            min_uct = node.children[0].reward / node.children[0].travel_num - math.sqrt(
                2 * math.log(node.travel_num) / node.children[0].travel_num)
        except ZeroDivisionError:
            return node.children[0]
        index = 0
        for c_index in range(len(node.children)):
            try:
                uct = node.children[c_index].reward / node.children[c_index].travel_num - math.sqrt(
                    2 * math.log(node.travel_num) / node.children[c_index].travel_num)
            except ValueError:
                uct = 0
            except ZeroDivisionError:
                return node.children[c_index]
            if uct < min_uct:
                min_uct = uct
                index = c_index
        return node.children[index]


class Node:

    def __init__(self, game_board, side):
        self.game_board = deepcopy(game_board)
        self.side = side
        self.children = []
        self.parent = None
        self.travel_num = 0
        self.reward = 0

    def expand(self):
        move_list = move_generate(self.game_board)
        for move in move_list:
            self.game_board.make_move(move, self.side)
            n = Node(self.game_board, -self.side)
            self.game_board.board[move[0]][move[1]] = NO_CHESS
            n.parent = self
            self.children.append(n)

    def simulate(self, side):
        temp_board = deepcopy(self.game_board)
        turn = self.side
        while temp_board.judge() is None:
            move_list = move_generate(temp_board)
            try:
                index = random.randint(0, len(move_list) - 1)
            except ValueError:
                return 0
            temp_board.make_move(move_list[index], turn)
            turn = -turn
        if side == temp_board.judge():
            return 1
        return 0

    def back_propagation(self, side):
        value = self.simulate(side)
        node = self
        while node is not None:
            node.travel_num += 1
            node.reward += value
            node = node.parent

    def select(self):
        node = self
        mode = 1
        while True:
            if not node.children:
                return node
            node = uct_select(node, mode)
            mode = -mode


class SearchEngine:

    def __init__(self, game_board, side, search_num=200):
        self.root = Node(game_board, side)
        self.root.expand()
        self.search_num = search_num

    def search(self):
        for _ in range(self.search_num + 1):
            self.pre_search()
        max_win_rate = self.root.children[0].reward / self.root.children[0].travel_num
        max_index = 0
        for index in range(len(self.root.children)):
            win_rate = self.root.children[index].reward / self.root.children[index].travel_num
            if win_rate > max_win_rate:
                max_win_rate = win_rate
                max_index = index
        print(max_win_rate)
        move_list = move_generate(self.root.game_board)
        return move_list[max_index]

    def pre_search(self):
        node = self.root.select()
        node.expand()
        node.back_propagation(self.root.side)


class AlphaBeta:

    def __init__(self, game_board, side):
        self.game_board = game_board
        self.side = side

    def search(self):
        move_list = move_generate(self.game_board)
        alpha = -10000000
        beta = 10000000
        while len(move_list):
            move = move_list.pop()
            self.game_board.make_move(move, self.side)
            val = -self.alpha_beta(3 - 1, -beta, -alpha, -self.side)
            self.game_board.board[move[0]][move[1]] = NO_CHESS
            if val > alpha:
                alpha = val
                best_move = deepcopy(move)
        print(alpha)
        return best_move

    def alpha_beta(self, depth, alpha, beta, minimax_player):
        if depth <= 0 or self.game_board.judge():
            value = evaluate(self.game_board, minimax_player)
            return value
        move_list = move_generate(self.game_board)
        while len(move_list):
            move = move_list.pop()
            self.game_board.make_move(move, minimax_player)
            val = -self.alpha_beta(depth - 1, -beta, -alpha, -minimax_player)
            self.game_board.board[move[0]][move[1]] = NO_CHESS
            if val >= beta:
                return beta
            if val > alpha:
                alpha = val
        return alpha
