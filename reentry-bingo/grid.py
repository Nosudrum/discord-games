from gridFunctions import plot_grid
from plotFunctions import start_earth_map, finish_figure

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Save figure
finish_figure(fig, "grid.png", show=True)