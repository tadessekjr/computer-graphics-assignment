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
        
def get_neighbors(r, c):

    neighbors = []

    if r > 0 and not visited[r - 1][c]:
        neighbors.append(("UP", r - 1, c))

    if r < ROWS - 1 and not visited[r + 1][c]:
        neighbors.append(("DOWN", r + 1, c))

    if c > 0 and not visited[r][c - 1]:
        neighbors.append(("LEFT", r, c - 1))

    if c < COLS - 1 and not visited[r][c + 1]:
        neighbors.append(("RIGHT", r, c + 1))

    return neighbors

def remove_wall(direction, r, c, nr, nc):

    if direction == "UP":
        northWall[r][c] = 0

    elif direction == "DOWN":
        northWall[nr][nc] = 0

    elif direction == "LEFT":
        eastWall[r][nc] = 0

    elif direction == "RIGHT":
        eastWall[r][c] = 0

def generate_maze():

    global current_row
    global current_col
    global generation_complete

    neighbors = get_neighbors(current_row, current_col)

    if neighbors:

        direction, nr, nc = random.choice(neighbors)

        stack.append((current_row, current_col))

        remove_wall(direction, current_row, current_col, nr, nc)

        current_row = nr
        current_col = nc

        visited[current_row][current_col] = True

        if random.randint(1, 20) == 1:

            directions = []

            if current_row > 0:
                directions.append(("UP", current_row - 1, current_col))

            if current_row < ROWS - 1:
                directions.append(("DOWN", current_row + 1, current_col))

            if current_col > 0:
                directions.append(("LEFT", current_row, current_col - 1))

            if current_col < COLS - 1:
                directions.append(("RIGHT", current_row, current_col + 1))

            if directions:

                d, rr, cc = random.choice(directions)

                remove_wall(
                    d,
                    current_row,
                    current_col,
                    rr,
                    cc
                )

    elif stack:

        current_row, current_col = stack.pop()

    else:

        generation_complete = True

        northWall[0][0] = 0
        eastWall[ROWS - 1][COLS - 1] = 0

def can_move(r, c, direction):

    if direction == "UP":

        return (
            r > 0 and
            northWall[r][c] == 0
        )

    elif direction == "DOWN":

        return (
            r < ROWS - 1 and
            northWall[r + 1][c] == 0
        )

    elif direction == "LEFT":

        return (
            c > 0 and
            eastWall[r][c - 1] == 0
        )

    elif direction == "RIGHT":

        return (
            c < COLS - 1 and
            eastWall[r][c] == 0
        )

    return False

def solve_maze():

    global solver_started
    global solver_finished
    global solver_row
    global solver_col

    if not solver_started:

        solver_stack.append((0, 0))
        solver_visited[0][0] = True

        solver_row = 0
        solver_col = 0

        solver_started = True

    if solver_row == ROWS - 1 and solver_col == COLS - 1:

        solver_finished = True
        return

    possible_moves = []

    directions = [
        ("UP", -1, 0),
        ("DOWN", 1, 0),
        ("LEFT", 0, -1),
        ("RIGHT", 0, 1)
    ]

    for direction, dr, dc in directions:

        nr = solver_row + dr
        nc = solver_col + dc

        if (
            0 <= nr < ROWS and
            0 <= nc < COLS and
            not solver_visited[nr][nc] and
            can_move(solver_row, solver_col, direction)
        ):

            possible_moves.append((nr, nc))

    if possible_moves:

        nr, nc = random.choice(possible_moves)

        solver_stack.append((nr, nc))

        solver_visited[nr][nc] = True

        solver_row = nr
        solver_col = nc

    else:

        dead_ends.append((solver_row, solver_col))

        solver_stack.pop()

        if solver_stack:

            solver_row, solver_col = solver_stack[-1]

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    if not generation_complete:

        generate_maze()

    elif not solver_finished:

        solve_maze()

    draw_maze()

    pygame.display.update()

pygame.quit()

