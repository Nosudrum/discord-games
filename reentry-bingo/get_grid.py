from math import ceil, floor
import numpy as np
from plotFunctions import alphabet


def flatten(list_of_lists):
    flattened_list = []
    for i in list_of_lists:
        for j in list_of_lists[i]:
            flattened_list.append(j)
    return flattened_list


def get_grid(lat_min, lat_max, nb_rows, nb_columns):
    lat_min = floor(lat_min)
    lat_max = ceil(lat_max)

    latitudes = np.linspace(lat_min, lat_max, nb_rows + 1)
    longitudes = np.linspace(-180, 180, nb_columns + 1)
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

    numbers_lon = (longitudes[1:] + longitudes[:-1]) / 2 - 4
    numbers_lat = (max(latitudes) + 2) * np.ones(len(numbers_lon))
    letters_lat = (latitudes[1:] + latitudes[:-1]) / 2 - 2
    letters_lon = (min(longitudes) + 9) * np.ones(len(letters_lat)) - 2
    letters = [alphabet[i] for i in range(nb_rows)]
    numbers = [str(i + 1) for i in range(nb_columns)]
    return points_lat, points_lon, numbers_lon, numbers_lat, letters_lon, letters_lat[::-1], numbers, letters, latitudes[::-1], longitudes
