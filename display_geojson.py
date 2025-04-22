import os
import json
from ipyleaflet import Map, GeoJSON
import ipywidgets as widgets

# define output for geojson data
info_output = widgets.Output()

m = Map(center=[39.926688, 7.930542], zoom=5.5)

with open("min_time_route.json") as f:
    data = json.load(f)

# function to display geojson data
def handle_click(event, feature, **kwargs):
    with info_output:
        info_output.clear_output()
        print("Information to this point:")
        for key, value in feature["properties"].items():
            if isinstance(value, dict) and "value" in value and "unit" in value:
                print(f"{key}: {value['value']} {value['unit']}")
            else:
                print(f"{key}: {value}")


# Add the GeoJSON layer
geo_json = GeoJSON(data=data)
geo_json.on_click(handle_click)

# Add the GeoJSON layer to the map
m.add(geo_json)
display(m, info_output)