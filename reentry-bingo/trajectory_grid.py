from TLEpropagation import lat, lon, t
import plotly.express as px
import plotly.graph_objects as go
from plotFunctions import remove_html_margins
import pandas as pd
from get_grid import get_grid

df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
df["marker_size"] = 1
deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
df["elapsed_hours"] = deltaT
fig1 = px.line_geo(df, lat="lat", lon="lon", hover_name="epoch", projection="mercator",
                   color_discrete_sequence=["#444444"])
fig2 = px.scatter_geo(df, lat="lat", lon="lon", hover_name="epoch", projection="mercator", color="elapsed_hours",
                      size_max=1)

grid_lat, grid_lon, numbers_lon, numbers_lat, letters_lon, letters_lat, numbers, letters = get_grid(df.lat.min(),
                                                                                                    df.lat.max(), 5, 20)
fig3 = px.line_geo(lat=grid_lat, lon=grid_lon, color_discrete_sequence=["white"])
grid = px.line_geo()
fig = go.Figure(data=fig1.data + fig2.data + fig3.data)

fig.update_layout(template="plotly_dark")
fig.write_html('trajectory.html')
remove_html_margins('trajectory.html')
