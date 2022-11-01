import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.image import imread
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

# from TLEpropagation import lat, lon, t
from get_grid import get_grid

# df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
# df["marker_size"] = 1
# deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
# df["elapsed_hours"] = deltaT

# lat_min = df.lat.min()
# lat_max = df.lat.max()

lat_min = -42
lat_max = 42

grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters, latitudes, longitudes = \
    get_grid(lat_min, lat_max, 5, 20)

columns_dict = {"Horodateur": "datetime", "What is your Discord username ?": "username", "Choose your row": "row",
                "Choose your column": "column"}
answers = pd.read_csv("answers.csv", parse_dates=['Horodateur']).rename(columns=columns_dict)
answers["zone"] = answers["row"] + answers["column"].map(str)
values = answers.zone.value_counts().values

color_map = cm.get_cmap('Oranges')
cmaplist = np.array([color_map(i) for i in range(color_map.N)])
cmaplist[:, -1] = 0.5

cmap = LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist.tolist(), color_map.N)
bounds = np.linspace(0, values.max() + 1, values.max() + 2)

fig = plt.figure(figsize=(10, 5), facecolor='black')
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
ax.set_global()
ax.imshow(imread('NE1_50M_SR_W.tif'), origin='upper', transform=ccrs.PlateCarree(),
          extent=[-180, 180, -90, 90])
ax.plot(grid_lon, grid_lat, color="white", transform=ccrs.PlateCarree())
for letter in enumerate(letters):
    ax.text(letters_lon[letter[0]], letters_lat[letter[0]], letter[1], color="white", transform=ccrs.PlateCarree(),
            weight='bold', fontsize=12)
for number in enumerate(numbers):
    ax.text(numbers_lon[number[0]], numbers_lat[number[0]], number[1], color="white", transform=ccrs.PlateCarree(),
            weight='bold', fontsize=12)

for row in enumerate(letters):
    for column in enumerate(numbers):
        letter = letters[row[0]]
        number = numbers[column[0]]
        zone = letter + str(number)
        value = (answers["zone"] == zone).sum()
        value_normalized = value / (values.max())
        color = cmap(value_normalized)
        latitudes_bounds = latitudes[row[0]:row[0] + 2]
        longitudes_bounds = longitudes[column[0]:column[0] + 2]
        latitudes_zone = [latitudes_bounds.min(), latitudes_bounds.max(), latitudes_bounds.max(),
                          latitudes_bounds.min()]
        longitudes_zone = [longitudes_bounds.min(), longitudes_bounds.min(), longitudes_bounds.max(),
                           longitudes_bounds.max()]
        ax.fill(longitudes_zone, latitudes_zone, color=color, transform=ccrs.PlateCarree())
sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=values.max()))

sm.set_array([])
cax = ax.inset_axes([0.15, 0.17, 0.7, 0.035])
cbar = fig.colorbar(sm, orientation="horizontal", cax=cax, boundaries=bounds, ticks=np.arange(0.5, values.max() + 1.5))
cbar.ax.set_xticklabels(np.arange(0, values.max() + 1))
cbar.ax.set_facecolor('none')

cbar.ax.tick_params(length=0)
# cbar.ax.xaxis.set_tick_params(color='white')
cbar.outline.set_edgecolor('white')
plt.setp(plt.getp(cbar.ax, 'xticklabels'), color='white', fontsize=12)

plt.tight_layout()

fig.savefig('heatmap.png', facecolor="None", edgecolor='none', dpi=300)
plt.show()
