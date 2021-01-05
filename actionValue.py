from typing import Dict
import pandas as pd
from state import State
import numpy as np
from collections.abc import Sequence


def get_key(state: State):
    return state.dealer + state.player * 100


class Q:
    def __init__(self, state: State):
        self.state = state
        self.N = 1
        self.nHits = 0
        self.nSticks = 0
        self.hitValue = 0
        self.stickValue = 0
        self.bestValue = 0

    def updateN(self, action):
        self.N += 1
        if action == "hit":
            self.nHits += 1
        else:
            self.nSticks += 1

    def updateQ(self, TotalReward, action):
        if action == "hit":
            self.hitValue += 1 / self.N * (TotalReward - self.hitValue)
        else:
            self.stickValue += 1 / self.N * (TotalReward - self.stickValue)

        self.bestValue = max([self.hitValue, self.stickValue])

    def __repr__(self):
        return str([self.state, self.N, self.bestValue])


class Experience:
    def __init__(self, N_0):
        self.N_0 = N_0
        self.QDict = {}  # Dict[int, Q]
        self.episode = []

    def update(self, state: State, action, reward=0):
        if state.terminal:
            for q in self.episode:
                q[0].updateQ(reward, q[1])
            self.episode = []

        else:
            key = get_key(state)
            if key in self.QDict:
                self.QDict[key].updateN(action)
            else:
                self.QDict[key] = Q(state)

            self.episode.append((self.QDict[key], action))

    def get_action(self, state):
        key = get_key(state)
        if key in self.QDict:
            eps = np.random.uniform()
            if eps < self.N_0 / (self.N_0 + self.QDict[key].N):
                if self.QDict[key].hitValue > self.QDict[key].stickValue:
                    return "hit"
                else:
                    if self.QDict[key].hitValue < self.QDict[key].stickValue:
                        return "stick"

        return np.random.choice(["hit", "stick"])

    def __repr__(self):
        return str(self.QDict)

    def get_V(self):
        V = np.zeros((10, 21))
        for qa in self.QDict:
            V[self.QDict[qa].state.dealer - 1, self.QDict[qa].state.player - 1] = self.QDict[qa].bestValue
        return V

    def get_V_df(self):
        keys = []
        values = []
        for qa in self.QDict:
            keys.append(qa)
            values.append(self.QDict[qa].bestValue)
        return pd.DataFrame({"state": keys, "V": values})

    def get_loss(self, V_opt):
        values = []
        opt_values = []
        for qa in self.QDict:
            values.append(self.QDict[qa].bestValue)
            opt_values.append(V_opt[V_opt["state"] == qa]["V"].values[0])
        if len(values) == V_opt.shape[0]:
            return np.linalg.norm(np.array(opt_values) - np.array(values)) ** 2
        else:
            return 10000
