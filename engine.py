from creature import Creature
import pygame
import random
import numpy as np
import random
import config
from metrics import Metrics

# --- Grid setup ---
grid = [[None for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]

# --- Creature setup ---
occupied = set()
creatures = []

while len(creatures) < config.NUM_CREATURES:
    x = random.randint(0, config.GRID_WIDTH - 1)
    y = random.randint(0, config.GRID_HEIGHT - 1)
    if (x, y) not in occupied:
        c = Creature(x, y)
        creatures.append(c)
        grid[y][x] = c
        occupied.add((x, y))

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Neuroevolution Demo Grid")
clock = pygame.time.Clock()

# --- Simulation setup ---
current_step = 0
current_generation = 0
metrics = Metrics()
metrics.end_of_generation_metrics(current_generation, creatures, config.NUM_CREATURES // 2, config.POSSIBLE_ACTIONS)



def evolve_population(creatures, num_creatures):
    # Select only creatures that ended up in the right half
    parents = [c for c in creatures if c.x >= config.GRID_WIDTH // 2]

    # Safety check: if no parents survived, fall back to all creatures
    if not parents:
        parents = creatures

    new_generation = []

    while len(new_generation) < num_creatures:
        parent = random.choice(parents)
        child = Creature(parent.x, parent.y)  # new creature at random spot later
        child.brain.weights = np.copy(parent.brain.weights)
        mutation = np.random.uniform(-0.05, 0.05, child.brain.weights.shape)
        child.brain.weights += mutation
        new_generation.append(child)

    return new_generation

def setup_generation_grid(creatures):
    grid = [[None for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
    occupied = set()
    for c in creatures:
        while True:
            x = random.randint(0, config.GRID_WIDTH - 1)
            y = random.randint(0, config.GRID_HEIGHT - 1)
            if (x, y) not in occupied:
                c.x, c.y = x, y
                grid[y][x] = c
                occupied.add((x, y))
                break
    return grid

# --- Engine loop ---
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
        # if current_generation < 10 and creature_index == 0:
        #     print(f"Phase 1 -- Generation {current_generation} Step {current_step} -- Creature {creature_index} wants to move to {p_x}, {p_y}")
        new_x = max(0, min(config.GRID_WIDTH-1, p_x))
        new_y = max(0, min(config.GRID_HEIGHT-1, p_y))
        moves.append((c, current_x, current_y, new_x, new_y))
        creature_index += 1

    # Phase 2: apply moves
    creature_index = 0
    for c, old_x, old_y, new_x, new_y in moves:
        grid[old_y][old_x] = None
        # if current_generation < 1 and creature_index < 2:
        #     print(f"Phase 2 Creature {creature_index} wants to move to {new_x}, {new_y}")
        #     print(f"Phase 2 Grid {new_x}, {new_y} is free if {grid[new_y][new_x] == None}")
        if grid[new_y][new_x] is None:  # only move if free
            c.x, c.y = new_x, new_y
            grid[new_y][new_x] = c
        else:
            # collision handling: stay put
            grid[old_y][old_x] = c
        if c.x >= config.GRID_WIDTH // 2:
            c.fitness += 1
        creature_index += 1


    # --- Draw ---
    screen.fill(config.BG_COLOR_LIGHT)  # black background
    for c in creatures:
        rect = pygame.Rect(c.x*config.CELL_SIZE, c.y*config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, c.get_color(), rect)  # green creatures

    pygame.display.set_caption(f"Neuroevolution Basic -- Generation {current_generation}")
    pygame.display.flip()

    current_step += 1
    if current_step >= config.STEPS_PER_GENERATION:
        current_generation += 1
        metrics.end_of_generation_metrics(current_generation, creatures, config.NUM_CREATURES // 2, config.POSSIBLE_ACTIONS)
        current_step = 0
        print(f"Generation {current_generation} finished")
        if(current_generation >= config.NUM_GENERATIONS):
            metrics.save_metrics()
            running = False;
        else:
            creatures = evolve_population(creatures, config.NUM_CREATURES)
            grid = setup_generation_grid(creatures)

    clock.tick(30)  # 30 FPS

pygame.quit()
