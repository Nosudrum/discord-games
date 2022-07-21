from TLEpropagation import lat, lon, t
import plotly.express as px
import plotly.graph_objects as go
from plotFunctions import remove_html_margins
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

df = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})

deltaT = (df.epoch - df.epoch[0]).dt.total_seconds() / 3600
df["elapsed_hours"] = deltaT
fig1 = px.line_geo(df, lat="lat", lon="lon", hover_name="epoch", projection="orthographic",
                   color_discrete_sequence=["#444444"])
fig2 = px.scatter_geo(df, lat="lat", lon="lon", hover_name="epoch", projection="orthographic", color="elapsed_hours")

grid = px.line_geo()
fig = go.Figure(data=fig1.data + fig2.data)

fig.update_layout(template="plotly_dark")
fig.write_html('trajectory.html')
remove_html_margins('trajectory.html')
