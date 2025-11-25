from creature import Creature
import pygame
import random
import numpy as np
import random
import config
from metrics import Metrics
from wolf import Wolf

# --- Grid setup ---
grid = [[None for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]

# --- Creature setup ---
occupied = set()
creatures = []
predators = []

while len(predators) < config.NUM_PREDATORS:
    x = random.randint(0, config.GRID_WIDTH - 1)
    y = random.randint(0, config.GRID_HEIGHT - 1)
    if (x, y) not in occupied:
        w = Wolf(x, y)
        predators.append(w)
        grid[y][x] = w
        occupied.add((x, y))


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
metrics.end_of_generation_metrics(current_generation, creatures, config.POSSIBLE_ACTIONS)



def evolve_population(creatures, num_creatures):
    # Sort by fitness (higher is better)
    creatures.sort(key=lambda c: c.fitness, reverse=True)

    # Select top 50% as parents
    num_parents = len(creatures) // 2
    parents = creatures[:num_parents]

    # Create new generation
    new_generation = []

    while len(new_generation) < num_creatures:
        parent = random.choice(parents)
        child = Creature(parent.x, parent.y)  # new creature at random spot later
        # Copy brain weights
        child.brain.weights = np.copy(parent.brain.weights)
        # Mutate slightly
        mutation = np.random.uniform(-0.05, 0.05, child.brain.weights.shape)
        child.brain.weights += mutation
        new_generation.append(child)

    return new_generation

def setup_generation_grid(creatures, predators):
    grid = [[None for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
    occupied = set()

    for w in predators:
        while True:
            x = random.randint(0, config.GRID_WIDTH - 1)
            y = random.randint(0, config.GRID_HEIGHT - 1)
            if (x, y) not in occupied:
                w = Wolf(x, y)
                grid[y][x] = w
                occupied.add((x, y))
                break


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
    key_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_pressed = True

    action_frame = not config.STEP_BY_STEP or (config.STEP_BY_STEP and key_pressed)
    if action_frame:
        # --- Update creatures ---
        wolf_moves = []
        wolf_index = 0
        for w in predators:
            current_x, current_y = w.x, w.y
            target = w.choose_target(creatures, grid)
            if(not target == None):
                p_x, p_y = w.propose_move(target)
                new_x = max(0, min(config.GRID_WIDTH-1, p_x))
                new_y = max(0, min(config.GRID_HEIGHT-1, p_y))
                if(config.PRINT_INFO and wolf_index == 0):
                    print(f"Phase 1 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} wants to move to {p_x}, {p_y}")
                wolf_moves.append((w, current_x, current_y, new_x, new_y))
            wolf_index += 1

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
            creature_index += 1
        
        wolf_index = 0
        for w, old_x, old_y, new_x, new_y in wolf_moves:
            if(config.PRINT_INFO and wolf_index == 0):
                print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} wants to move to {new_x}, {new_y}")
            grid[old_y][old_x] = None
            at_spot = grid[new_y][new_x]

            if config.STEP_BY_STEP and action_frame: 
                print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} wants to move to {new_x}, {new_y}")
                if(isinstance(w.current_target, Creature)):
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} targetting {w.current_target.x}, {w.current_target.y}")
                else:
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} has no target")


            if grid[new_y][new_x] is None:
                if((config.PRINT_INFO and wolf_index == 0) or (config.STEP_BY_STEP and action_frame)):
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} should move to empty space")
                w.x, w.y = new_x, new_y
                grid[new_y][new_x] = w
                if config.STEP_BY_STEP and action_frame: 
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} moved to {new_x}, {new_y}")
                    if(isinstance(w.current_target, Creature)):
                        print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf target adj {w.is_target_adjacent(w.current_target)} and isolated {w.current_target.is_isolated(grid)}")
                if(isinstance(w.current_target, Creature) and w.is_target_adjacent(w.current_target) and w.current_target.is_isolated(grid)):
                    w.current_target.get_killed(grid)
            elif isinstance(at_spot, Creature) and at_spot.is_isolated(grid):
                if((config.PRINT_INFO and wolf_index == 0) or (config.STEP_BY_STEP and action_frame)):
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} moved onto non-target isolated creature for a kill")
                at_spot.get_killed(grid)
                w.x, w.y = new_x, new_y
                grid[new_y][new_x] = w 
            else:
                grid[old_y][old_x] = w
                if((config.PRINT_INFO and wolf_index == 0) or (config.STEP_BY_STEP and action_frame)):
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} blocked by another wolf or non-isolated creature")
            if(config.PRINT_INFO and wolf_index == 0):
                    print(f"Phase 2 -- Generation {current_generation} Step {current_step} -- Wolf {wolf_index} went from {old_x},{old_y} to {new_x},{new_y}")
            wolf_index += 1

    # --- Draw ---
    screen.fill(config.BG_COLOR_LIGHT)  # black background
    for c in creatures:
        if(c.alive):
            rect = pygame.Rect(c.x*config.CELL_SIZE, c.y*config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
            pygame.draw.rect(screen, c.get_color(), rect)  # green creatures

    for w in predators:
        rect = pygame.Rect(w.x*config.CELL_SIZE, w.y*config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, config.WOLF_COLOR, rect) 

    pygame.display.set_caption(f"Neuroevolution Basic -- Generation {current_generation}")
    pygame.display.flip()

    if action_frame:
        current_step += 1
        if current_step >= config.STEPS_PER_GENERATION:
            current_generation += 1
            metrics.end_of_generation_metrics(current_generation, creatures, config.POSSIBLE_ACTIONS)
            current_step = 0
            print(f"Generation {current_generation} finished")
            if(current_generation >= config.NUM_GENERATIONS):
                metrics.save_metrics()
                running = False;
            else:
                creatures = evolve_population(creatures, config.NUM_CREATURES)
                grid = setup_generation_grid(creatures, predators)

    clock.tick(30)  # 30 FPS

pygame.quit()
