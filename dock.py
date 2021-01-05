import numpy as np


def pick():
    color = np.random.choice(["red", "black"], p=[1 / 3, 1 - 1 / 3])
    if color == "black":
        return np.random.choice(range(1, 11))
    else:
        return - np.random.choice(range(1, 11))

def pick_first():
     return np.random.choice(range(1,11))