from datetime import datetime, timezone, timedelta

import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.image import imread

from TLEpropagation import lat, lon, t
from get_grid import get_grid

df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
df["marker_size"] = 1
deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
df["elapsed_hours"] = deltaT

window_mid = datetime(2022, 7, 30, 16, 55, 00, tzinfo=timezone.utc)
window_half_range = timedelta(hours=1.3)

impact_lon = 119
impact_lat = 9.1

time_start = window_mid - window_half_range

df_before = df[(df.lon < impact_lon) & (df.epoch > time_start) & (df.epoch < window_mid + timedelta(minutes=5))]


grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters, latitudes, longitudes = \
    get_grid(df.lat.min(), df.lat.max(), 5, 20)

columns_dict = {"Horodateur": "datetime", "What is your Discord username ?": "username", "Choose your row": "row",
                "Choose your column": "column"}
answers = pd.read_csv("answers.csv", parse_dates=['Horodateur']).rename(columns=columns_dict)
answers["zone"] = answers["row"] + answers["column"].map(str)
values = answers.zone.value_counts().values

color_map = cm.get_cmap('Oranges')

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
        color = color_map(value_normalized)
        latitudes_bounds = latitudes[row[0]:row[0] + 2]
        longitudes_bounds = longitudes[column[0]:column[0] + 2]
        latitudes_zone = [latitudes_bounds.min(), latitudes_bounds.max(), latitudes_bounds.max(),
                          latitudes_bounds.min()]
        longitudes_zone = [longitudes_bounds.min(), longitudes_bounds.min(), longitudes_bounds.max(),
                           longitudes_bounds.max()]
        ax.fill(longitudes_zone, latitudes_zone, color=color, transform=ccrs.PlateCarree(), alpha=0.5)
ax.plot(df_before.lon, df_before.lat, '.', color="blue", transform=ccrs.PlateCarree(), markersize=0.5)
ax.plot(impact_lon, impact_lat, '*', color="red", transform=ccrs.PlateCarree(), markersize=7)
plt.tight_layout()

fig.savefig('trajectory_heatmap_impact.png', facecolor="None", edgecolor='none', dpi=300)
plt.show()