import numpy as np
from collections import Counter
import math
import csv

import config

class Metrics:
    def __init__(self):
        self.metrics_log = []

    def save_metrics(self):
        with open("metrics.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.metrics_log[0].keys())
            writer.writeheader()
            writer.writerows(self.metrics_log)

    def end_of_generation_metrics(self, current_generation, creatures, num_reproducers, actions):
        metrics_for_generation = {}
        metrics_for_generation["num_reproducers"] = int(num_reproducers)
        metrics_for_generation["right_half"] = self.count_right_half(creatures)
        metrics_for_generation["diversity_radius"] = self.compute_diversity_radius(creatures)
        metrics_for_generation["behavioral_entropy"] = self.compute_behavioral_entropy(creatures, actions)
        metrics_for_generation["generation"] = current_generation
        self.metrics_log.append(metrics_for_generation)
    
    def flatten_weights(self, brain):
        return brain.weights.reshape(-1)

    def compute_diversity_radius(self,creatures):
        W = np.stack([self.flatten_weights(c.brain) for c in creatures])  # shape: (N, D)
        centroid = np.mean(W, axis=0)                                # (D,)
        dists = np.linalg.norm(W - centroid, axis=1)                 # (N,)
        return float(np.mean(dists))                                 # ≥ 0

    def compute_behavioral_entropy(self, creatures, actions):
        # dominant action per creature
        dom = []
        for c in creatures:
            strengths = np.mean(c.brain.weights, axis=0)             # (num_actions,)
            idx = int(np.argmax(strengths))
            dom.append(actions[idx])
        # histogram
        counts = Counter(dom)
        N = len(creatures)
        probs = [counts[a]/N for a in actions]
        # entropy (natural log)
        eps = 1e-12
        H = -sum(p * math.log(p + eps) for p in probs)               # ≥ 0
        return H
    
    def count_right_half(self, creatures):
        count = 0
        for c in creatures:
            if c.x >= config.GRID_WIDTH // 2:
                count += 1
        return count

    
