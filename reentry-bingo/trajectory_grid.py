from datetime import datetime, timezone, timedelta

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.image import imread

from TLEpropagation import lat, lon, t
from get_grid import get_grid

df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
df["marker_size"] = 1
deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
df["elapsed_hours"] = deltaT

window_mid = datetime(2022, 11, 5, 2, 21, 00, tzinfo=timezone.utc)
window_half_range = timedelta(hours=16)

df_before = df[(df.epoch < window_mid) & (df.epoch > window_mid - window_half_range)]
df_after = df[(df.epoch > window_mid) & (df.epoch < window_mid + window_half_range)]
impact_lon = (df_before.tail(1).lon.values[0] + df_after.head(1).lon.values[0]) / 2
impact_lat = (df_before.tail(1).lat.values[0] + df_after.head(1).lat.values[0]) / 2

grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters, latitudes, longitudes = \
    get_grid(df.lat.min(), df.lat.max(), 5, 20)

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
ax.plot(df_before.lon, df_before.lat, '.', color="blue", transform=ccrs.PlateCarree(), markersize=0.5)
ax.plot(df_after.lon, df_after.lat, '.', color="red", transform=ccrs.PlateCarree(), markersize=0.5)
ax.plot(impact_lon, impact_lat, 'o', color="orange", transform=ccrs.PlateCarree(), markersize=7)
plt.tight_layout()

fig.savefig('trajectory_grid.png', facecolor="None", edgecolor='none', dpi=300)
plt.show()
