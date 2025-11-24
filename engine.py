import pygame
import random


# --- Grid setup ---
CELL_SIZE = 6
GRID_WIDTH = 128
GRID_HEIGHT = 128
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
BG_COLOR_LIGHT = (224, 223, 206)

# --- Creature setup ---
NUM_CREATURES = 1000
creatures = []

for _ in range(NUM_CREATURES):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    creatures.append([x, y])

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Neuroevolution Demo Grid")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update creatures (random walk for now) ---
    for c in creatures:
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1), (0,0)])
        c[0] = max(0, min(GRID_WIDTH-1, c[0] + dx))
        c[1] = max(0, min(GRID_HEIGHT-1, c[1] + dy))

    # --- Draw ---
    screen.fill(BG_COLOR_LIGHT)  # black background
    for c in creatures:
        rect = pygame.Rect(c[0]*CELL_SIZE, c[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (30, 89, 10), rect)  # green creatures

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
