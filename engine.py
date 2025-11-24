from creature import Creature
import pygame
import random


# --- Grid setup ---
CELL_SIZE = 6
GRID_WIDTH = 128
GRID_HEIGHT = 128
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
BG_COLOR_LIGHT = (224, 223, 206)
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# --- Creature setup ---
NUM_CREATURES = 1000
occupied = set()
creatures = []

while len(creatures) < NUM_CREATURES:
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    if (x, y) not in occupied:
        c = Creature(x, y)
        creatures.append(c)
        grid[y][x] = c
        occupied.add((x, y))

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Neuroevolution Demo Grid")
clock = pygame.time.Clock()

# --- Simulation setup ---
STEPS_PER_GENERATION = 30
NUM_GENERATIONS = 20

current_step = 0
current_generation = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update creatures ---
    moves = []
    creature_index = 0
    for c in creatures:
        current_x, current_y = c.x, c.y
        action = c.decide(c.sense(grid))
        p_x, p_y = c.propose_move(action)
        if current_generation < 1 and creature_index < 2:
            print(f"Phase 1 Creature {creature_index} wants to move to {p_x}, {p_y}")
        new_x = max(0, min(GRID_WIDTH-1, p_x))
        new_y = max(0, min(GRID_HEIGHT-1, p_y))
        moves.append((c, current_x, current_y, new_x, new_y))
        creature_index += 1

    # Phase 2: apply moves
    creature_index = 0
    for c, old_x, old_y, new_x, new_y in moves:
        grid[old_y][old_x] = None
        if current_generation < 1 and creature_index < 2:
            print(f"Phase 2 Creature {creature_index} wants to move to {new_x}, {new_y}")
            print(f"Phase 2 Grid {new_x}, {new_y} is free if {grid[new_y][new_x] == None}")
        if grid[new_y][new_x] is None:  # only move if free
            c.x, c.y = new_x, new_y
            grid[new_y][new_x] = c
        else:
            # collision handling: stay put
            grid[old_y][old_x] = c
        creature_index += 1


    # --- Draw ---
    screen.fill(BG_COLOR_LIGHT)  # black background
    for c in creatures:
        rect = pygame.Rect(c.x*CELL_SIZE, c.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (30, 89, 10), rect)  # green creatures

    pygame.display.flip()

    current_step += 1
    if current_step >= STEPS_PER_GENERATION:
        current_generation += 1
        current_step = 0
        print(f"Generation {current_generation} finished")
        if(current_generation >= NUM_GENERATIONS):
            running = False;

    clock.tick(30)  # 30 FPS

pygame.quit()
