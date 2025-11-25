import numpy as np
from brain import Brain
import config


class Creature:
    def __init__(self, x, y, allowed_actions=None, allowed_sensors=None, brain=None):
        self.x = x
        self.y = y
        self.alive = True
        self.actions = allowed_actions or [1]*len(config.POSSIBLE_ACTIONS)
        self.sensors = allowed_sensors or [1]*len(config.POSSIBLE_SENSORS)
        self.brain = brain or Brain(self._input_size(), len(config.POSSIBLE_ACTIONS)) # neural net or rule set
        self.fitness = 0

    def _input_size(self):
        size = 0
        for s in config.POSSIBLE_SENSORS:
            if s == "DIST_WALLS":
                size += 4
            else:
                size += 1
        return size
    
    def get_killed(self, grid):
        grid[self.y][self.x] = None
        self.alive = False
        self.x = -1
        self.y = -1
        

    def sense(self, grid):
        inputs = []
        for i, s in enumerate(config.POSSIBLE_SENSORS):
            if not self.sensors[i]:
                # Sensor disabled → feed a neutral value (e.g. 0)
                if s == "DIST_WALLS":
                    inputs.extend([0,0,0,0])  # 4 zeros for the 4 walls
                else:
                    inputs.append(0)
                continue

            # Sensor enabled → collect real data
            if s in ["N","S","E","W","NE","NW","SE","SW"]:
                inputs.append(self._check_neighbor(grid, s))
            elif s == "DIST_WALLS":
                inputs.extend(self._distance_to_walls(grid))
        return inputs
    
    def _check_neighbor(self, grid, direction):
        dx, dy = self._action_to_delta(direction)
        nx, ny = self.x + dx, self.y + dy

        # Stay inside bounds
        if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
            return 1  # treat out-of-bounds as "occupied"

        return 1 if grid[ny][nx] is not None else 0
    
    def _distance_to_walls(self, grid):
        height = len(grid)
        width = len(grid[0])

        # Raw distances
        dist_north = self.y
        dist_south = height - 1 - self.y
        dist_west  = self.x
        dist_east  = width - 1 - self.x

        # Normalize to [0,1]
        norm_north = dist_north / (height - 1)
        norm_south = dist_south / (height - 1)
        norm_west  = dist_west  / (width - 1)
        norm_east  = dist_east  / (width - 1)

        return [norm_north, norm_south, norm_west, norm_east]


    def decide(self, inputs):
        action_index = self.brain.predict(inputs, config.POSSIBLE_ACTIONS)
        return config.POSSIBLE_ACTIONS[action_index]

    def propose_move(self, action):
        dx, dy = self._action_to_delta(action)
        # Proposed move, world will handle clamping
        return self.x + dx, self.y + dy
    
    def _action_to_delta(self, action):
        mapping = {
            "N":  (0, -1),
            "S":  (0,  1),
            "E":  (1,  0),
            "W":  (-1, 0),
            "NE": (1, -1),
            "NW": (-1,-1),
            "SE": (1,  1),
            "SW": (-1, 1),
            "STAY": (0, 0)
        }
        return mapping.get(action, (0,0))

    def get_color(self):
        # Average weights per action (collapse inputs dimension)
        # action_strengths = np.mean(self.brain.weights, axis=0)
        # dominant_index = int(np.argmax(action_strengths))
        # dominant_action = config.POSSIBLE_ACTIONS[dominant_index]
        # return config.ACTION_COLORS[dominant_action]
        return config.SINGLE_CREATURE_COLOR
    
    def is_isolated(self, grid):
        # Offsets for the 8 surrounding cells
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]
        
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            # Bounds check if grid is a 2D array
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbor = grid[nx][ny]
                if isinstance(neighbor, Creature):
                    # Found a non-wolf neighbor → not isolated
                    return False
        return True

 
