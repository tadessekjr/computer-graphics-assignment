import pygame
import random

pygame.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")

clock = pygame.time.Clock()

northWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]
eastWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]

visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

stack = []

current_row = 0
current_col = 0

visited[current_row][current_col] = True

generation_complete = False

solver_stack = []
solver_visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

dead_ends = []

solver_started = False
solver_finished = False

solver_row = 0
solver_col = 0
def draw_maze():

    screen.fill(WHITE)

    for (r, c) in dead_ends:

        pygame.draw.rect(
            screen,
            BLUE,
            (
                c * CELL_SIZE + 5,
                r * CELL_SIZE + 5,
                CELL_SIZE - 10,
                CELL_SIZE - 10
            )
        )

    for (r, c) in solver_stack:

        pygame.draw.rect(
            screen,
            GREEN,
            (
                c * CELL_SIZE + 8,
                r * CELL_SIZE + 8,
                CELL_SIZE - 16,
                CELL_SIZE - 16
            )
        )

    for row in range(ROWS):
        for col in range(COLS):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if northWall[row][col]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x, y),
                    (x + CELL_SIZE, y),
                    2
                )

            if eastWall[row][col]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    2
                )

    pygame.draw.line(
        screen,
        BLACK,
        (0, 0),
        (0, HEIGHT),
        2
    )

    pygame.draw.line(
        screen,
        BLACK,
        (0, HEIGHT),
        (WIDTH, HEIGHT),
        2
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (5, 5, CELL_SIZE - 10, CELL_SIZE - 10)
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            (COLS - 1) * CELL_SIZE + 5,
            (ROWS - 1) * CELL_SIZE + 5,
            CELL_SIZE - 10,
            CELL_SIZE - 10
        )
    )

    if not generation_complete:
        pygame.draw.circle(
            screen,
            RED,
            (
                current_col * CELL_SIZE + CELL_SIZE // 2,
                current_row * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 4
        )

    if solver_started and not solver_finished:

        pygame.draw.circle(
            screen,
            BLACK,
            (
                solver_col * CELL_SIZE + CELL_SIZE // 2,
                solver_row * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 4
        )
