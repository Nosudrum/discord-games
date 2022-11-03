from datetime import datetime, timezone

import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import requests
from skyfield.api import EarthSatellite, load, wgs84

from codeModules.inputParser import window_mid, window_half_range, debris_international_designator, impact_lat, impact_lon


def get_propagation_duration(sat_epoch_utc_datetime):
    propagation_end = window_mid + window_half_range
    if propagation_end < datetime.now(timezone.utc):
        print("ERROR : Propagation end is in the past. Stopping.")
        exit()
    else:
        propagation_duration = propagation_end - sat_epoch_utc_datetime
        propagation_duration_days = np.ceil(propagation_duration.total_seconds() / 86400)
        print(f"TLE propagation duration : {propagation_duration_days} days")
        return propagation_duration_days


URL = f"https://celestrak.org/NORAD/elements/gp.php?INTDES={debris_international_designator}&FORMAT=tle"

TLE = requests.get(URL).text.splitlines()

if TLE[0] == 'No GP data found':
    print("WARNING : No online TLE found. Using local TLE file.")
    with open('../TLE_backup.txt', mode='r') as infile:
        TLE = infile.read().splitlines()
else:
    print("TLE found. Using online TLE and updating local file.")
    with open('../TLE_backup.txt', 'w') as outfile:
        for line in TLE:
            outfile.write(f"{line}\n")

sat = EarthSatellite(TLE[1], TLE[2], TLE[0].strip())

ts = load.timescale()
t = ts.tt_jd(np.arange(sat.epoch.tt, sat.epoch.tt + get_propagation_duration(sat.epoch.utc_datetime()), 1 / 86400))

# Compute geocentric positions for the satellite.
geocentric = sat.at(t)
lat, lon = wgs84.latlon_of(geocentric)

trajectory = pd.DataFrame({"lat": lat.degrees, "lon": lon.degrees, "epoch": t.utc_datetime()})
trajectory["marker_size"] = 1
deltaT = (trajectory.epoch - trajectory.epoch[0]).dt.total_seconds() / 3600
trajectory["elapsed_hours"] = deltaT

trajectory_before = trajectory[
    (trajectory.epoch < window_mid) & (trajectory.epoch > window_mid - window_half_range)]
trajectory_after = trajectory[(trajectory.epoch > window_mid) & (trajectory.epoch < window_mid + window_half_range)]


def get_impact_point():
    if impact_lat is None or impact_lon is None:
        impact_lon_estimated = (trajectory_before.tail(1).lon.values[0] + trajectory_after.head(1).lon.values[0]) / 2
        impact_lat_estimated = (trajectory_before.tail(1).lat.values[0] + trajectory_after.head(1).lat.values[0]) / 2
        return impact_lat_estimated, impact_lon_estimated
    else:
        return impact_lat, impact_lon


def plot_trajectory(ax):
    impact_lat_plot, impact_lon_plot = get_impact_point()
    ax.plot(trajectory_before.lon, trajectory_before.lat, '.', color="blue", transform=ccrs.PlateCarree(),
            markersize=0.5)
    ax.plot(trajectory_after.lon, trajectory_after.lat, '.', color="red", transform=ccrs.PlateCarree(), markersize=0.5)
    ax.plot(impact_lon_plot, impact_lat_plot, 'o', color="orange", transform=ccrs.PlateCarree(), markersize=7)
