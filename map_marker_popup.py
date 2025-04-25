import os
import json
from ipyleaflet import Map, GeoJSON, Popup
import ipywidgets as widgets
from ipywidgets import HTML
from IPython.display import display

# define output for geojson data
info_output = widgets.Output()


with open("min_time_route.json") as f:
    data = json.load(f)

# function to display geojson data
def display_marker_popup(event, feature, map):
    props = feature['properties']
    coordinates = feature['geometry']['coordinates'][::-1]
    coordinates[0] += 0.45
    # Nur bestimmte Infos anzeigen
    time = props.get("time", {})
    time_text = time

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
        location=coordinates,
        child=popup_content,
        close_button=True,
        auto_close=False,
        close_on_escape_key=True
    ) 
    map.add(popup)

def add_geojson_to_map(geojson_data, map):
     # GeoJSON-Layer erstellen
    geo_json = GeoJSON(data=geojson_data, name='Route')
    
    # Klick-Event-Handler setzen
    geo_json.on_click(lambda event, feature, **kwargs: display_marker_popup(event, feature, map))
    
    # GeoJSON-Layer zur Karte hinzufügen
    map.add(geo_json)