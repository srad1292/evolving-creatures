# Grid Properties
CELL_SIZE = 6
GRID_WIDTH = 128
GRID_HEIGHT = 128

# Window Properties
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Simulation Properties
NUM_CREATURES = 1000
STEPS_PER_GENERATION = 200
NUM_GENERATIONS = 30

# Basic Colors
BG_COLOR_LIGHT = (224, 223, 206)

# Creature Colors
ACTION_COLORS = {
    "N":    (0, 0, 255),      # blue
    "S":    (255, 0, 0),      # red
    "E":    (0, 255, 0),      # green
    "W":    (255, 255, 0),    # yellow
    "NE":   (0, 255, 255),    # cyan
    "NW":   (255, 0, 255),    # magenta
    "SE":   (128, 255, 0),    # lime
    "SW":   (255, 128, 0),    # orange
    "STAY": (128, 128, 128),  # gray
}
