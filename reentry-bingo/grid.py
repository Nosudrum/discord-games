from codeModules.gridFunctions import plot_grid, debris_international_designator
from codeModules.plotFunctions import start_earth_map, finish_figure

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Save figure
finish_figure(fig, f"plots/{debris_international_designator}_grid.png", show=False)
