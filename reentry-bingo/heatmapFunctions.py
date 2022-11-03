import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from gridFunctions import get_grid
from input_parser import colormap

# MODIFY THIS SETUP TO MATCH YOUR DATA
answers_path = "answers.csv"
columns_dict = {"Horodateur": "datetime", "What is your Discord username ?": "username", "Choose your row": "row",
                "Choose your column": "column"}
answers = pd.read_csv(answers_path, parse_dates=['Horodateur']).rename(columns=columns_dict)
answers["zone"] = answers["row"] + answers["column"].map(str)
values = answers.zone.value_counts().values


def plot_heatmap(fig, ax):
    _, _, _, _, _, _, numbers, letters, latitudes, longitudes = get_grid()
    color_map = cm.get_cmap(colormap)
    for row in enumerate(letters):
        for column in enumerate(numbers):
            letter = letters[row[0]]
            number = numbers[column[0]]
            zone = letter + str(number)
            value = (answers["zone"] == zone).sum()
            value_normalized = value / (values.max())
            color = color_map(value_normalized)
            latitudes_bounds = latitudes[row[0]:row[0] + 2]
            longitudes_bounds = longitudes[column[0]:column[0] + 2]
            latitudes_zone = [latitudes_bounds.min(), latitudes_bounds.max(), latitudes_bounds.max(),
                              latitudes_bounds.min()]
            longitudes_zone = [longitudes_bounds.min(), longitudes_bounds.min(), longitudes_bounds.max(),
                               longitudes_bounds.max()]
            ax.fill(longitudes_zone, latitudes_zone, color=color, transform=ccrs.PlateCarree(), alpha=0.5)

    # Setup colorbar
    color_map_list = np.array([color_map(i) for i in range(color_map.N)])
    color_map_list[:, -1] = 0.5
    custom_map = LinearSegmentedColormap.from_list(
        'Custom cmap', color_map_list.tolist(), color_map.N)
    bounds = np.linspace(0, values.max() + 1, values.max() + 2)
    sm = cm.ScalarMappable(cmap=custom_map, norm=plt.Normalize(vmin=0, vmax=values.max()))
    sm.set_array([])
    cax = ax.inset_axes([0.15, 0.17, 0.7, 0.035])
    cbar = fig.colorbar(sm, orientation="horizontal", cax=cax, boundaries=bounds,
                        ticks=np.arange(0.5, values.max() + 1.5))
    cbar.ax.set_xticklabels(np.arange(0, values.max() + 1))
    cbar.ax.set_facecolor('none')
    cbar.ax.tick_params(length=0)
    cbar.outline.set_edgecolor('white')
    plt.setp(plt.getp(cbar.ax, 'xticklabels'), color='white', fontsize=12)
