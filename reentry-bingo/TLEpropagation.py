import numpy as np
from skyfield.api import EarthSatellite, load, wgs84
import requests

URL = "https://celestrak.org/NORAD/elements/gp.php?INTDES=2022-143B&FORMAT=tle"

TLE = requests.get(URL).text.splitlines()

sat = EarthSatellite(TLE[1], TLE[2], TLE[0].strip())

ts = load.timescale()
t = ts.tt_jd(np.arange(sat.epoch.tt, sat.epoch.tt + 4.0, 1 / 86400))

# Compute geocentric positions for the satellite.

geocentric = sat.at(t)
lat, lon = wgs84.latlon_of(geocentric)
