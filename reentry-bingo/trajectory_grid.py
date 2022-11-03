from gridFunctions import plot_grid
from plotFunctions import start_earth_map, finish_figure
from trajectoryFunctions import plot_trajectory

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Plot trajectory
plot_trajectory(ax)

# Save figure
finish_figure(fig, "trajectory_grid.png", show=True)
