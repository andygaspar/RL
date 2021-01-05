from step_fun import step
import dock
from state import State
from actionValue import Q,Experience
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

qvalues = Experience(100)
actions = ["hit", "stick"]


def episode():
    player = dock.pick_first()
    dealer = dock.pick_first()
    state = State(dealer, player)
    while True:
        action = qvalues.get_action(state)
        qvalues.update(state, action)
        state, reward = step(state, action)
        if state.terminal:
            break
    qvalues.update(state, action, reward)

df_opt = pd.read_csv("V_opt.csv")
for i in range(3000000):
    episode()
    if i % 1000 == 0:
        print(i,qvalues.get_loss(df_opt))

qvalues.get_V()
#
df = qvalues.get_V_df()
df.to_csv("V_opt.csv")

plt.imshow(qvalues.get_V())
plt.show()

qvals = qvalues.get_V()

val_xdim, val_ydim = qvals.shape

# generate meshgrid for plot
xax = np.arange(1, val_xdim+1)
yax = np.arange(1, val_ydim+1)
xax, yax = np.meshgrid(yax, xax)


# plot and save
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(xax, yax, qvals, rstride=1, cstride=1, cmap='viridis', linewidth=0, antialiased=False)
ax.plot_wireframe(xax, yax, qvals, color='k', lw=0.05, alpha=0.3)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
plt.savefig("100_000.png", dpi=160)