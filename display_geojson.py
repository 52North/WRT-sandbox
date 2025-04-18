import os
import json
from ipyleaflet import Map, GeoJSON
import ipywidgets as widgets

m = Map(center=[39.926688, 7.930542], zoom=5.5)

with open("min_time_route.json") as f:
    data = json.load(f)

def handle_click(event, feature, **kwargs):
    with info_output:
        info_output.clear_output()
        print("Information to this point:")
        for key, value in feature["properties"].items():
            print(f"{key}: {value}")


# Add the GeoJSON layer
geo_json = GeoJSON(data=data)
geo_json.on_click(handle_click)

# Add the GeoJSON layer to the map
m.add(geo_json)
display(m, info_output)