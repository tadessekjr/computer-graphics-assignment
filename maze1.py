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

