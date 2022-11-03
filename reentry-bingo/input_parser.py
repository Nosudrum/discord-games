import csv
from datetime import datetime, timedelta

with open('input_settings.csv', mode='r') as infile:
    reader = csv.reader(infile)
    input_settings = {}
    for rows in reader:
        data = rows[1]
        if data == 'None':
            data = None
        elif rows[0] == 'window_mid':
            data = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")
        elif rows[0] == 'window_half_range':
            data = datetime.strptime(data, "%H:%M:%S")
            data = timedelta(hours=data.hour, minutes=data.minute, seconds=data.second)
        elif rows[0] == 'impact_lat' or rows[0] == 'impact_lon':
            data = float(data)
        elif rows[0] != 'colormap' and rows[0] != 'debris_international_designator':
            data = int(data)
        input_settings[rows[0]] = data

grid_lat_min = input_settings['grid_lat_min']
grid_lat_max = input_settings['grid_lat_max']
grid_lon_min = input_settings['grid_lon_min']
grid_lon_max = input_settings['grid_lon_max']
colormap = input_settings['colormap']
nb_rows = input_settings['nb_rows']
nb_columns = input_settings['nb_columns']
debris_international_designator = input_settings['debris_international_designator']
window_mid = input_settings['window_mid']
window_half_range = input_settings['window_half_range']
impact_lat = input_settings['impact_lat']
impact_lon = input_settings['impact_lon']
