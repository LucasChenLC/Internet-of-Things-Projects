WHITE_CHESS = 1     # 白棋宏定义
BLACK_CHESS = -1    # 黑棋宏定义
NO_CHESS = 0        # 空白宏定义

NO_WINNER = 0       # 游戏未结束
WHITE_WIN = 1       # 白棋胜利
BLACK_WIN = -1      # 黑棋胜利


class Position:     # 位置类

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Chess(object):    # 棋子类

    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y
