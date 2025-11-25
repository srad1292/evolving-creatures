import random


class Wolf:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_target = None

    # There are not enough creatures for me to bother doing BFS and dealing with bounds, etc so 
    # just loop through creatures and find nearest using same logic as king's piece movement in chess: Chebyshev distance 
    def find_nearest(self, creatures):
        nearest = None
        nearest_dist = float("inf")
        for creature in creatures:
            if not creature.alive:
                continue
            dist = self._calculate_distance(creature)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = creature
        return nearest
    
    # First pass using only above method causes wolves to go idle and stick to grouped targets
    def choose_target(self, creatures, grid):
    # First look for isolated creatures
        isolated_targets = [c for c in creatures if c.alive and c.is_isolated(grid)]
        if isolated_targets:
            nearest_isolated = min(isolated_targets, key=lambda c: self._calculate_distance(c))
            self.current_target = nearest_isolated
            return nearest_isolated
        
        # Otherwise chase nearest creature
        nearest = self.find_nearest(creatures)
        if nearest and not nearest.is_isolated(grid):
            # 50% chance to roam randomly instead of sticking
            if random.random() < 0.5:
                self.current_target = None
                return None  # signal to roam
        self.current_target = nearest
        return nearest
    
    def _calculate_distance(self, creature):
        dx = abs(self.x - creature.x)
        dy = abs(self.y - creature.y)
        dist = max(dx, dy)
        return dist  
    
    def propose_move(self, creature):
        if creature is None:
            step_x = random.choice([-1,0,1])
            step_y = random.choice([-1,0,1])
            return self.x + step_x, self.y + step_y
        else:
            dx = creature.x - self.x
            dy = creature.y - self.y
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
            p_x = self.x + step_x 
            p_y = self.y + step_y 
            return p_x, p_y
    
    def is_target_adjacent(self, creature):
        if creature is None:
            return False
        dist = self._calculate_distance(creature)
        return dist == 1


