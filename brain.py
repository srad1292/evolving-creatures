import random
import numpy as np

class Brain:
    def __init__(self, num_inputs, num_actions):
        # self.weights = weights or self._random_weights()
        self.weights = np.random.uniform(-0.1, 0.1, (num_inputs, num_actions))

    def predict(self, inputs, actions):
        # Convert inputs to numpy vector
        x = np.array(inputs)
        # Linear combination: inputs × weights → action scores
        scores = x @ self.weights   # shape: (num_actions,)
        # Pick the action with the highest score
        return int(np.argmax(scores))

