import numpy as np
from skyfield.api import EarthSatellite, load, wgs84

with open('TLE_test.txt', 'r') as f:
    tle = f.read().split("\n")
    f.close()

tle = [x.strip() for x in tle]

sat = EarthSatellite(tle[1], tle[2], tle[0])

ts = load.timescale()
t = ts.tt_jd(np.arange(sat.epoch.tt, sat.epoch.tt + 3.0, 1/(24*60)))

# Compute geocentric positions for the satellite.

geocentric = sat.at(t)
lat, lon = wgs84.latlon_of(geocentric)