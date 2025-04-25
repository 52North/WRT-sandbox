import os
import json
from ipyleaflet import Map, GeoJSON, Popup
import ipywidgets as widgets
from ipywidgets import HTML
from IPython.display import display

# define output for geojson data
info_output = widgets.Output()

m = Map(center=[39.926688, 7.930542], zoom=5.5)

with open("min_time_route.json") as f:
    data = json.load(f)

# function to display geojson data
def handle_click(event, feature, **kwargs):
    props = feature['properties']
    
    # Nur bestimmte Infos anzeigen
    time = props.get("time", {})
    time_text = f"{time.get('value', '–')} {time.get('unit', '')}"

    fuel = props.get("fuel_consumption", {})
    fuel_text = f"{fuel.get('value', '–')} {fuel.get('unit', '')}"

    speed = props.get("speed", {})
    speed_text = f"{speed.get('value', '–')} {speed.get('unit', '')}"

    power = props.get("engine_power", {})
    power_text = f"{power.get('value', '–')} {power.get('unit', '')}"

    # HTML für das Popup
    popup_content = HTML()
    popup_content.value = f"""
        <b>Time:</b> {time_text}<br>
        <b>Fuel consumption:</b> {fuel_text}<br>
        <b>Speed:</b> {speed_text}<br>
        <b>Engine power:</b> {power_text}
    """

    # Popup erstellen
    popup = Popup(
        location=event['coordinates'],
        child=popup_content,
        close_button=True,
        auto_close=False,
        close_on_escape_key=True
    ) 
    m.add(popup)

# GeoJSON-Layer erstellen und Callback setzen
geo_json = GeoJSON(data=data, name='Route')
geo_json.on_click(handle_click)


# Add the GeoJSON layer to the map
m.add(geo_json)
display(m, info_output)