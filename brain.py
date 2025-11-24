import random

class Brain:
    def __init__(self, weights=None):
        # self.weights = weights or self._random_weights()
        self.weights = weights

    def predict(self, inputs, actions):
        # For now, random
        return random.randint(0, len(actions) - 1)

