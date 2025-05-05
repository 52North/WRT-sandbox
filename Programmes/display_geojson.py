import os
import json
from ipyleaflet import Map, GeoJSON, Popup
from IPython.display import display
import matplotlib.pyplot as plt
from map_marker_popup import add_geojson_to_map

m = Map(center=[39.926688, 7.930542], zoom=5.5)

with open("/home/jovyan/Data/min_time_route.json") as f:
    data = json.load(f)

add_geojson_to_map(data, m)

display(m)