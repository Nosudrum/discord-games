from codeModules.gridFunctions import plot_grid, debris_international_designator
from codeModules.plotFunctions import start_earth_map, finish_figure
from codeModules.trajectoryFunctions import plot_trajectory

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Plot trajectory
plot_trajectory(ax, up_to_impact=None)

# Save figure
finish_figure(fig, f"plots/{debris_international_designator}_trajectory_grid.png", show=False)
