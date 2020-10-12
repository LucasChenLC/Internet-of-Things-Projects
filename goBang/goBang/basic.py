WHITE_CHESS = 1
BLACK_CHESS = -1
NO_CHESS = 0

NO_WINNER = 0
WHITE_WIN = 1
BLACK_WIN = -1


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Chess(object):
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y
