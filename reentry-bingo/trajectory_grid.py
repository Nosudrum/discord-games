from codeModules.gridFunctions import plot_grid
from codeModules.plotFunctions import start_earth_map, finish_figure
from codeModules.trajectoryFunctions import plot_trajectory

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Plot trajectory
plot_trajectory(ax)

# Save figure
finish_figure(fig, "plots/trajectory_grid.png", show=False)
