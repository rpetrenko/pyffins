import numpy as np
from collections import OrderedDict

from base.snake import Snake
from base.food import Food


def generate_symbols(length):
    min_char = ord('A')
    max_char = ord('Z')
    assert length <= max_char - min_char + 1, "maximum of 26 symbols supported"
    return [chr(min_char + i) for i in range(length)]


class Game(object):
    def __init__(self, height, width, s_empty="_", periodic=None):
        """
        :param height:
        :param width:
        :param symbols:
        """
        self.h = height
        self.w = width
        self.s_empty = s_empty
        # self.symbols = [self.s_empty]
        self.board = np.full([height, width], ord(self.s_empty))
        self.snakes = list()
        self.food = None
        self.update = []
        self.periodic = periodic

    def _is_empty(self, x, y):
        return ord(self.s_empty) == self.board[x][y]

    def _is_food(self, x, y):
        return ord(self.food.symbol) == self.board[x][y]

    def _get_empty(self):
        res = []
        for x in range(self.board.shape[0]):
            for y in range(self.board.shape[1]):
                if self._is_empty(x, y):
                    res.append((x, y))
        return res

    def _is_another_snake(self, snake_symbol, x, y):
        if self._is_food(x, y) or self._is_empty(x, y) or snake_symbol == chr(self.board[x][y]):
            return False
        else:
            return True

    def create_snakes(self, num_snakes, snake_length):
        snake_symbols = generate_symbols(num_snakes)
        for snake_symbol in snake_symbols:
            points = np.zeros((snake_length, 2), dtype=np.uint16)
            points.fill(np.nan)
            snake = Snake(points, symbol=snake_symbol)
            self.snakes.append(snake)

    def create_food(self, n_foods):
        points = np.zeros((n_foods, 2), dtype=np.int16)
        points.fill(np.nan)
        self.food = Food(symbol="*")

    def get_board(self):
        lines = []
        for i in range(self.board.shape[0]):
            lines.append([chr(x) for x in self.board[i]])
        return lines

    def get_food_points(self):
        return list(zip(*np.where(self.board == ord(self.food.symbol))))

    def print_board(self):
        lines = self.get_board()
        for line in lines:
            s = " ".join(line)
            print(s)
        print()

    def place_food(self, nfood):
        v = ord(self.food.symbol)
        empty_cells = self._get_empty()
        np.random.shuffle(empty_cells)
        for x, y in empty_cells:
            self.board[x][y] = v
            self.food.nfood += 1
            if nfood == self.food.nfood:
                return True
        return False

    def place_snake(self, snake):
        v = ord(snake.symbol)
        empty_cells = self._get_empty()
        # shuffle empty cells
        np.random.shuffle(empty_cells)
        cur_len = 0
        #TODO place a snake for length > 1
        for x, y in empty_cells:
            self.board[x][y] = v
            snake.points[cur_len][0] = x
            snake.points[cur_len][1] = y
            cur_len += 1
            if cur_len == snake.length:
                return True
        return False

    def print_snakes(self):
        print()
        for snake in self.snakes:
            print(snake)

    def set_board(self, x, y, symbol):
        self.board[x][y] = ord(symbol)
        self.update.append((x, y, symbol))

    def _make_periodic(self, x, y):
        if x < 0:
            x = self.h - 1
        elif x == self.h:
            x = 0
        elif y < 0:
            y = self.w - 1
        elif y == self.w:
            y = 0
        return [x, y]

    def _outside(self, x, y):
        return x < 0 or x == self.h or y < 0 or y == self.w

    def snake_dies(self, snake):
        # no moves, snake dies
        for x, y in snake.points:
            self.set_board(x, y, self.food.symbol)
        self.food.nfood += snake.length
        snake.killme()

    def _inside(self, x, y):
        return 0 <= x < self.h and 0 <= y < self.w

    def get_points_around(self, point, step=1):
        assert step == 1, "larger neighbors not implemented"
        x, y = point
        r1 = []
        for i in range(x-step, x+step+1):
            for j in range(y-step, y+step+1):
                if x == i and y == j:
                    # exclude self
                    continue
                if x != i and y != j:
                    # exclude diagonals
                    continue
                if self._inside(i, j):
                    r1.append([i, j])
        return r1

    def snakes_dead(self):
        return all([x.dead for x in self.snakes])

    def make_update(self):
        self.update = []
        for snake in self.snakes:
            if snake.dead:
                continue
            x, y = snake.points[0]
            x_tail, y_tail = snake.points[-1]
            moves = [
                [x, y + 1], # right
                [x, y - 1], # left
                [x + 1, y], # down
                [x - 1, y]  # up
            ]
            # weight = -1, means snake dies
            weights = np.array([-1] * 4)
            for i in range(4):
                x_new, y_new = moves[i]
                if self.periodic:
                    # periodic boundary
                    x_new, y_new = self._make_periodic(x_new, y_new)
                    moves[i] = [x_new, y_new]
                if 0 <= x_new < self.h and 0 <= y_new < self.w:
                    # find best move
                    s = chr(self.board[x_new][y_new])
                    if s == snake.symbol:
                        # itself
                        weight = -1
                    elif s == self.s_empty:
                        # empty cell
                        weight = 1
                    elif s == self.food.symbol:
                        # food
                        weight = 10
                    else:
                        # another snake
                        weight = -1
                else:
                    # out of bounds
                    weight = -1
                weights[i] = weight

            # get best move, if several moves have the same weight,
            # then choose randomly one
            imoves = np.argwhere(weights == np.amax(weights)).ravel()
            if imoves.shape[0] > 1:
                np.random.shuffle(imoves)
            imove = imoves[0]
            if weights[imove] == -1:
                self.snake_dies(snake)
            else:
                # we have a move, proceed
                x_new, y_new = moves[imove]
                # erase tail if new cell is not food
                if self.board[x_new][y_new] != ord(self.food.symbol):
                    # cut last tail cell
                    self.set_board(x_tail, y_tail, self.s_empty)
                    snake.points = np.concatenate(([[x_new, y_new]], snake.points[:-1]))
                else:
                    # snake ate food cell
                    snake.points = np.concatenate(([[x_new, y_new]], snake.points))
                    self.food.nfood -= 1
                self.set_board(x_new, y_new, snake.symbol)

            # kill snake if it touches the other snake
            points = self.get_points_around(snake.points[0], step=1)
            if points:
                for x, y in points:
                    if self._is_another_snake(snake.symbol, x, y):
                        self.snake_dies(snake)


def init_game(height,
              width,
              num_snakes,
              snake_length,
              n_foods,
              s_empty=" ",
              periodic=False
              ):
    game = Game(height, width, s_empty=s_empty, periodic=periodic)
    game.create_snakes(num_snakes, snake_length)
    game.create_food(n_foods)
    # place snakes
    for snake in game.snakes:
        assert game.place_snake(snake), "can't place a snake"
    # place food
    assert game.place_food(n_foods), "can't place all food"
    return game


if __name__ == "__main__":
    height = 5
    width = 10
    num_snakes = 1
    snake_length = 1
    n_foods = 49

    game = init_game(height, width, num_snakes, snake_length, n_foods, s_empty="_")

    frame = 0
    print(frame)
    game.print_board()
    while not game.snakes_dead():
        frame += 1
        print(frame)
        game.make_update()
        game.print_board()
