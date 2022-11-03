from codeModules.gridFunctions import plot_grid
from codeModules.plotFunctions import start_earth_map, finish_figure

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Save figure
finish_figure(fig, "plots/grid.png", show=True)
