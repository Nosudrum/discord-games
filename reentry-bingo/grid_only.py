from TLEpropagation import lat, lon, t
import plotly.express as px
from plotFunctions import remove_html_margins, alphabet
import pandas as pd
from get_grid import get_grid

import matplotlib.pyplot as plt
from matplotlib.image import imread
import cartopy.crs as ccrs

df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
df["marker_size"] = 1
deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
df["elapsed_hours"] = deltaT

grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters, latitudes, longitudes = \
    get_grid(df.lat.min(), df.lat.max(), 5, 20)
# fig = px.line_geo(lat=grid_lat, lon=grid_lon, color_discrete_sequence=["white"])
#
# fig.update_layout(template="plotly_dark", hovermode=False)
# fig.write_html('grid_only.html')
# # fig.write_image('grid_only.png')
# remove_html_margins('grid_only.html')

fig = plt.figure(figsize=(10, 5), facecolor='black')
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
ax.set_global()
# ax.stock_img()
ax.imshow(imread('NE1_50M_SR_W.tif'), origin='upper', transform=ccrs.PlateCarree(),
          extent=[-180, 180, -90, 90])
ax.plot(grid_lon, grid_lat, color="white", transform=ccrs.PlateCarree())
for letter in enumerate(letters):
    ax.text(letters_lon[letter[0]], letters_lat[letter[0]], letter[1], color="white", transform=ccrs.PlateCarree(),
            weight='bold', fontsize=12)
for number in enumerate(numbers):
    ax.text(numbers_lon[number[0]], numbers_lat[number[0]], number[1], color="white", transform=ccrs.PlateCarree(),
            weight='bold', fontsize=12)
plt.tight_layout()

fig.savefig('grid_only.png', facecolor="None", edgecolor='none', dpi=300)
plt.show()
