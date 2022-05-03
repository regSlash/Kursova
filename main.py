import time
import pygame
from opensimplex import OpenSimplex



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

fullscreen = False
size = (800, 800)
corners = False
square_size = 20
weight = 2
xy_off = 0.2

def scale(x):
    return 1 if x > 0 else 0

pygame.init()

if fullscreen:
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size=size)

clock = pygame.time.Clock()

tmp = OpenSimplex()
z_off = 0

running = True
while running:
    t1 = time.perf_counter()
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            running = False

    grid = [[scale(tmp.noise3(x=j * xy_off, y=i * xy_off, z=z_off)) for j in range(size[0] // square_size + 1)] for i in range(size[1] // square_size + 1)]

    z_off += 0.01

    screen.fill(GREY)

    if corners:
        for row_i, row in enumerate(grid):
            for col_i, cell in enumerate(row):
                pygame.draw.circle(screen, WHITE if cell == 1 else BLACK, (col_i*square_size, row_i*square_size), weight*2)

    for i in range(len(grid) - 1):
        for j in range(len(grid[0]) - 1):
            a = (int(square_size * (j + 0.5)), int(square_size * i))
            b = (int(square_size * (j + 1)), int(square_size * (i + 0.5)))
            c = (int(square_size * (j + 0.5)), int(square_size * (i + 1)))
            d = (int(square_size * j), int(square_size * (i + 0.5)))

            x = (
                grid[i][j]
                + 2 * grid[i][j + 1]
                + 4 * grid[i + 1][j + 1]
                + 8 * grid[i + 1][j]
            )
            if x in (1, 10, 14):
                pygame.draw.line(screen, WHITE, a, d, weight)
            if x in (2, 5, 13): #2 5 13
                pygame.draw.line(screen, WHITE, a, b, weight)
            if x in (4, 10, 11): #4 10 11
                pygame.draw.line(screen, WHITE, b, c, weight)
            if x in (5, 7, 8): # 5 7 8
                pygame.draw.line(screen, WHITE, c, d, weight)
            if x in (3, 12): # 3 12
                pygame.draw.line(screen, WHITE, b, d, weight)
            if x in (6, 9): #6 9
                pygame.draw.line(screen, WHITE, a, c, weight)

    pygame.display.flip()
    print("FPS:", 1 / (time.perf_counter() - t1))
    clock.tick(60)

pygame.quit()