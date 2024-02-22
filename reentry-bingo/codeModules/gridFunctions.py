import cartopy.crs as ccrs
import numpy as np

from codeModules.inputParser import grid_lat_min, grid_lat_max, grid_lon_min, grid_lon_max, nb_rows, nb_columns, \
    debris_international_designator
from codeModules.trajectoryFunctions import trajectory

# It is recommended to set a fixed latitude range for the grid, to avoid the grid changing when the window shrinks.
# For the first run, when the latitude range might not be known, set it to None in the input file.
if grid_lat_min is None:
    grid_lat_min = np.floor(trajectory.lat.min())
    print(f"WARNING : grid_lat_min set to None, using {grid_lat_min}°.")
if grid_lat_max is None:
    grid_lat_max = np.ceil(trajectory.lat.max())
    print(f"WARNING : grid_lat_max set to None, using {grid_lat_max}°.")
if grid_lon_min is None:
    grid_lon_min = np.floor(trajectory.lon.min())
    print(f"WARNING : grid_lon_min set to None, using {grid_lon_min}°.")
if grid_lon_max is None:
    grid_lon_max = np.ceil(trajectory.lon.max())
    print(f"WARNING : grid_lon_max set to None, using {grid_lon_max}°.")

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_grid():
    latitudes = np.linspace(grid_lat_min, grid_lat_max, nb_rows + 1)
    longitudes = np.linspace(grid_lon_min, grid_lon_max, nb_columns + 1)
    grid_lon = np.meshgrid(longitudes, latitudes)[0]
    grid_lat = np.meshgrid(longitudes, latitudes)[1]

    points_lat = []
    points_lon = []

    for row in range(nb_rows + 1):
        points_lat += grid_lat[row, :].tolist()
        if row % 2 == 1:
            points_lon += grid_lon[row, ::-1].tolist()
        else:
            points_lon += grid_lon[row, :].tolist()

    if (nb_rows + 1) % 2 == 1:  # end on the right
        for column in reversed(range(nb_columns + 1)):
            points_lon += grid_lon[:, column].tolist()
            if column % 2 == 1:
                points_lat += grid_lat[:, column].tolist()
            else:
                points_lat += grid_lat[::-1, column].tolist()

    else:  # end on the left
        for column in range(nb_columns + 1):
            points_lon += grid_lon[:, column].tolist()
            if column % 2 == 1:
                points_lat += grid_lat[:, column].tolist()
            else:
                points_lat += grid_lat[::-1, column].tolist()

    numbers_lon = (longitudes[1:] + longitudes[:-1]) / 2 - 8
    numbers_lat = (max(latitudes) + 2) * np.ones(len(numbers_lon))
    letters_lat = (latitudes[1:] + latitudes[:-1]) / 2 - 2
    letters_lon = (min(longitudes) + 9) * np.ones(len(letters_lat)) - 2
    letters = [alphabet[i] for i in range(nb_rows)]
    numbers = [str(i + 1) for i in range(nb_columns)]
    return points_lat, points_lon, numbers_lon, numbers_lat, letters_lon, letters_lat[
                                                                          ::-1], numbers, letters, latitudes[
                                                                                                   ::-1], longitudes


def plot_grid(axes):
    grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters, _, _ = get_grid()
    axes.plot(grid_lon, grid_lat, color="white", transform=ccrs.PlateCarree())
    for letter in enumerate(letters):
        axes.text(letters_lon[letter[0]], letters_lat[letter[0]], letter[1], color="white",
                  transform=ccrs.PlateCarree(), weight='bold', fontsize=12)
    for number in enumerate(numbers):
        axes.text(numbers_lon[number[0]], numbers_lat[number[0]], number[1], color="white",
                  transform=ccrs.PlateCarree(), weight='bold', fontsize=12)
