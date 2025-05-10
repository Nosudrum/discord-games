from datetime import timedelta

import warnings
from linecache import cache

import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import requests
from skyfield.api import EarthSatellite, load, wgs84

from codeModules.inputParser import window_mid, window_half_range, debris_international_designator, impact_lat, \
    impact_lon, impact_time


def is_impact_time_known():
    if impact_time is None:
        return False
    else:
        return True


def get_propagation_duration(sat_epoch_utc_datetime):
    if is_impact_time_known():
        if sat_epoch_utc_datetime > impact_time:
            print("ERROR: Satellite epoch is after impact time. Stopping")
            exit()
        else:
            propagation_duration = impact_time - sat_epoch_utc_datetime
            propagation_duration_days = np.ceil(propagation_duration.total_seconds() / 86400)
            print(f"TLE propagation duration : {propagation_duration_days} days")
            return propagation_duration_days
    propagation_end = window_mid + window_half_range
    if sat_epoch_utc_datetime > propagation_end:
        print("ERROR : Satellite epoch is after propagation end. Stopping.")
        exit()
    else:
        propagation_duration = propagation_end - sat_epoch_utc_datetime
        propagation_duration_days = np.ceil(propagation_duration.total_seconds() / 86400)
        print(f"TLE propagation duration : {propagation_duration_days} days")
        return propagation_duration_days


URL = f"https://celestrak.org/NORAD/elements/gp-last.php?INTDES={debris_international_designator}&FORMAT=TLE"

try:
    TLE = requests.get(URL).text.splitlines()
    if TLE[0] == 'No GP data found':
        raise ValueError
    print("TLE found. Using online TLE and updating local file.")
    with open('TLE_backup.txt', 'w') as outfile:
        for line in TLE:
            outfile.write(f"{line}\n")
except (requests.exceptions.ConnectTimeout, ValueError):
    print("WARNING : No online TLE found. Using local TLE file.")
    with open('TLE_backup.txt', mode='r') as infile:
        TLE = infile.read().splitlines()

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


if impact_lon is not None:
    trajectory_before = trajectory[
         (trajectory.epoch > (window_mid - window_half_range)) & (
                trajectory.epoch < window_mid + timedelta(minutes=5))]
else:
    trajectory_before = trajectory[
        (trajectory.epoch < window_mid) & (trajectory.epoch > window_mid - window_half_range)]
trajectory_after = trajectory[(trajectory.epoch > window_mid) & (trajectory.epoch < window_mid + window_half_range)]


def is_impact_location_known():
    if impact_lat is None or impact_lon is None:
        return False
    else:
        return True


def get_impact_point():
    if is_impact_location_known():
        return impact_lat, impact_lon
    elif is_impact_time_known():
        impact_point_1 = trajectory[(trajectory.epoch < impact_time)].tail(1)
        impact_point_2 = trajectory[(trajectory.epoch > impact_time)].head(1)
        impact_interp_epochs = [pd.Timestamp(impact_point_1.epoch.values[0]).timestamp(),
                                pd.Timestamp(impact_point_2.epoch.values[0]).timestamp()]
        impact_interp_lat = [impact_point_1.lat.values[0], impact_point_2.lat.values[0]]
        impact_interp_lon = [impact_point_1.lon.values[0], impact_point_2.lon.values[0]]
        impact_lat_estimated = np.interp(impact_time.timestamp(), impact_interp_epochs, impact_interp_lat)
        impact_lon_estimated = np.interp(impact_time.timestamp(), impact_interp_epochs, impact_interp_lon)
        return impact_lat_estimated, impact_lon_estimated
    else:
        impact_lon_estimated = (trajectory_before.tail(1).lon.values[0] + trajectory_after.head(1).lon.values[0]) / 2
        impact_lat_estimated = (trajectory_before.tail(1).lat.values[0] + trajectory_after.head(1).lat.values[0]) / 2
        return impact_lat_estimated, impact_lon_estimated


def plot_window_trajectory(ax):
    impact_lat_plot, impact_lon_plot = get_impact_point()
    ax.plot(trajectory_before.lon, trajectory_before.lat, '.', color="blue", transform=ccrs.PlateCarree(),
            markersize=0.5)
    ax.plot(trajectory_after.lon, trajectory_after.lat, '.', color="red", transform=ccrs.PlateCarree(),
            markersize=0.5)
    ax.plot(impact_lon_plot, impact_lat_plot, 'o', color="orange", transform=ccrs.PlateCarree(), markersize=7)


def plot_impact_trajectory(ax):
    impact_lat_plot, impact_lon_plot = get_impact_point()
    end_time = window_mid if impact_time is None else impact_time
    trajectory_before_impact = trajectory[(trajectory.epoch > (end_time - timedelta(hours=1.5))) & (
                trajectory.epoch < end_time)]
    ax.plot(trajectory_before_impact.lon, trajectory_before_impact.lat, '.', color="blue", transform=ccrs.PlateCarree(),
            markersize=0.5)
    ax.plot(impact_lon_plot, impact_lat_plot, '*', color="red", transform=ccrs.PlateCarree(), markersize=7)


def plot_trajectory(ax, up_to_impact=None):
    if up_to_impact is None:
        if is_impact_location_known() or is_impact_time_known():
            plot_impact_trajectory(ax)
        else:
            plot_window_trajectory(ax)
    else:
        if up_to_impact:
            plot_impact_trajectory(ax)
        else:
            plot_window_trajectory(ax)
