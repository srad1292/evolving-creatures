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
NUM_GENERATIONS = 50

# Network options
POSSIBLE_ACTIONS = ["N","S","E","W","NE","NW","SE","SW","STAY"]
POSSIBLE_SENSORS = ["N","S","E","W","NE","NW","SE","SW","DIST_WALLS"]

# Basic Colors
BG_COLOR_LIGHT = (224, 223, 206)

# Creature Colors
# Green for east
# Blue for north
# Yellow for south
# Red for west
# Middle of two for the diagonals
# Grey for still
ACTION_COLORS = {
    "N":    (15, 34, 112),    # Dark Blue
    "S":    (157, 146, 16),   # Yellow
    "E":    (30, 89, 0),      # Dark Green
    "W":    (174, 25, 25),    # Dark Red
    "NE":   (66, 250, 192),   # Blue / Green Mix
    "NW":   (246, 77, 255),   # Blue / Red Mix
    "SE":   (198, 252, 53),    # Yellow / Green Mix
    "SW":   (250, 184, 77),   # Yellow / Red Mix
    "STAY": (128, 128, 128),  # gray
}
