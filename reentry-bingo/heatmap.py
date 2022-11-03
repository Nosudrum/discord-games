from gridFunctions import plot_grid
from heatmapFunctions import plot_heatmap
from plotFunctions import start_earth_map, finish_figure

# Plot Earth map
fig, ax = start_earth_map()

# Plot grid
plot_grid(ax)

# Plot heatmap
plot_heatmap(fig, ax)

# Save figure
finish_figure(fig, "plots/heatmap.png", show=True)
