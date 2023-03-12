import pygame
import pygame as pg

W, H = 600, 600

BLACK = (0, ) * 3
GRAY = (100, ) * 3
WHITE = (225, ) * 3
RED = (225, 0, 0)
YELLOW = (225, 225, 0)
LIGHTGREEN = (0, 200, 200)

CROSS = '#046582'
CIRCLE = '#e4bad4'

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Крестики-Нолики")


def draw_circle(sc, x, y, size):
    x = (x + .5) * size
    y = (y + .5) * size
    pg.draw.circle(sc, CIRCLE, (x, y), (size - 3) // 2, 3)


def draw_cross(sc, x, y, size):
    x = x * size + 3
    y = y * size + 3
    pg.draw.line(sc, CROSS, (x, y), (x + size - 3, y + size - 3), 3)
    pg.draw.line(sc, CROSS, (x + size - 3, y - 3), (x, y + size - 3), 3)

def is_end(board):
    check_i_line = lambda x, i: True if x[i][0] == x[i][1] == x[i][2] != 0 else False
    check_i_col = lambda x, i: True if x[0][i] == x[1][i] == x[2][i] != 0 else False
    check_main_diag = lambda x: True if x[0][0] == x[1][1] == x[2][2] != 0 else False
    check_secondary_diag = lambda x: True if x[0][2] == x[1][1] == x[2][0] != 0 else False

    for i in range(3):
        if check_i_col(board, i):
            return 'col', i
        if check_i_line(board, i):
            return 'line', i
        if check_main_diag(board):
            return 'diag', 1
        if check_secondary_diag(board):
            return 'diag', 2
        return None

class Board:
    def __init__(self, W, H, size):
        self.W = W
        self.H = H
        self.size = size
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.mode = 1

    def click(self, mouse_pos):
        x = mouse_pos[0] // self.size
        y = mouse_pos[1] // self.size
        self.board[y][x] = self.mode
        self.mode = -self.mode

    def render(self, sc):
        pg.draw.line(sc, GRAY, (0, 200), (self.W, 200))
        pg.draw.line(sc, GRAY, (0, 400), (self.W, 400))
        pg.draw.line(sc, GRAY, (200, 0), (200, self.H))
        pg.draw.line(sc, GRAY, (400, 0), (400, self.H))
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 1:
                    draw_cross(sc, x, y, self.size)
                elif self.board[y][x] == -1:
                    draw_circle(sc, x, y, self.size)

    def check_end(self):
        is_end_info = is_end(self.board)
        shift = self.W // 10
        if is_end_info is not None:
            type_end = is_end_info[0]
            number = is_end_info[1]
            if type_end == 'col':
                x0, y0 = (number + .5) * self.size, shift
                x1, y1 = (number + .5) * self.size, self.size * 3 - shift
            elif type_end == 'line':
                x0, y0 = shift, (number + .5) * self.size
                x1, y1 = 3 * self.size - shift, (number + .5) * self.size
            elif type_end == 'diag':
                if number == 1:
                    x0, y0 = shift, shift
                    x1, y1 = 3 * self.size - shift, 3 * self.size - shift
                else:
                    x0, y0 = 3 * self.size - shift, shift
                    x1, y1 = shift, 3 * self.size - shift
            pg.draw.line(screen, RED, (x0, y0), (x1, y1), 10)
            pg.display.update()
            pg.time.delay(3000)
            return True
        else:
            return False


board = Board(W, H, 200)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            board.click(event.pos)
    screen.fill(WHITE)
    board.render(screen)
    board.check_end()
    pg.display.update()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        exit()
