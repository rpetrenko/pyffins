import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import base as b


def run_game():
    board_w = 120
    board_h = 30
    info_w = 10
    height = board_h + 2
    width = board_w + info_w + 2
    delay = 100
    num_snakes = 26
    num_snakes = min(num_snakes, height - 3)
    snake_length = 1
    n_food = 26 * 40
    n_food = min(n_food, board_h*board_w - num_snakes)
    curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    win = curses.newwin(height, width, 0, 0)
    win.keypad(1)
    win.border(0)
    win.nodelay(1)

    game = b.game.init_game(board_h, board_w, num_snakes, snake_length, n_food)

    def draw_board():
        for s in game.snakes:
            for x, y in s.points:
                win.addch(x+1, y+1, s.symbol)
        for x, y in game.get_food_points():
            win.addch(x+1, y+1, game.food.symbol)

    def draw_info(frame):
        msg = "[{},{}] frame:{}".format(board_h, board_w, frame)
        win.addstr(0, 2, msg)
        first_y = board_w + 3
        x, y = 1, first_y
        for s in game.snakes:
            msg = "{}:{:3}".format(s.symbol, s.length)
            if s.dead:
                msg = "{}-".format(msg)
            win.addstr(x, y, msg)
            x += 1
        msg = "{}:{:3}".format(game.food.symbol, game.food.length)
        win.addstr(height-2, first_y, msg)
        all_dead = all([x.dead for x in game.snakes])
        return all_dead

    def update_board():
        if game.update:
            for x, y, s in game.update:
                win.addch(x+1, y+1, s)

    frame = 1
    draw_board()
    draw_info(frame)

    key = None
    while key not in [27, ord('q')]:
        if key is not None:
            if key == ord('a'):
                win.timeout(delay)
            game.make_update()
            update_board()
            frame += 1
            all_dead = draw_info(frame)
            if all_dead:
                key = None
            if key == ord('n'):
                key = None

        event = win.getch()
        key = key if event == -1 else event

    curses.endwin()


if __name__ == "__main__":
    run_game()
