from datetime import datetime
import os
import json
from ipyleaflet import Map, GeoJSON, Popup
import ipywidgets as widgets
from ipywidgets import HTML
from IPython.display import display

# define output for geojson data
info_output = widgets.Output()

def calculate_cumulative_fuel(geojson_data):
    features = geojson_data.get('features', [])
    cumulative_fuel = 0.0
    cumulative_fuel_list=[]
    for i in range(len(features) - 1):  # letzten Punkt auslassen
        curr = features[i]
        next_f = features[i + 1]

        try:
            t1 = datetime.strptime(curr['properties']['time'], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(next_f['properties']['time'], "%Y-%m-%d %H:%M:%S")
            dt_hours = (t2 - t1).total_seconds() / 3600.0

            fuel_rate = curr['properties']['fuel_consumption']['value']
            if fuel_rate >= 0:
                fuel_used = fuel_rate * dt_hours
            else:
                fuel_used = 0.0  # negative Werte ignorieren
            cumulative_fuel_list[i]=cumulative_fuel
            cumulative_fuel += fuel_used
        except Exception as e:
            cumulative_fuel += 0.0  # im Fehlerfall keine Änderung
    return cumulative_fuel_list
# function to display geojson data
def display_marker_popup(event, feature, map, fuel_list):
    from IPython import get_ipython
    shell = get_ipython()
    active_popups = shell.user_ns.get('active_popups', [])

    props = feature['properties']
    coordinates = feature['geometry']['coordinates'][::-1]
    #coordinates[0] += 0.45
    # Nur bestimmte Infos anzeigen
    time = props.get("time", {})
    time_text = time

    fuel = props.get("fuel_consumption", {})
    fuel_text = f"{fuel.get('value', '–')} {fuel.get('unit', '')}"

    speed = props.get("speed", {})
    speed_text = f"{speed.get('value', '–')} {speed.get('unit', '')}"

    power = props.get("engine_power", {})
    power_text = f"{power.get('value', '–')} {power.get('unit', '')}"

    acc_fuel_text=f"{fuel_list[feature.get("id")] + "t"}"
   
    # HTML für das Popup
    popup_content = HTML()
    popup_content.value = f"""
        <div style="margin-top:-10px">
            <b>Time:</b> {time_text}<br>
            <b>Fuel consumption:</b> {fuel_text}<br>
            <b>Speed:</b> {speed_text}<br>
            <b>Engine power:</b> {power_text}
            <b>Cumulative fuel: </b> {acc_fuel_text}<br>
        </div>
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
    active_popups.append(popup)

    # Update the global list
    shell.user_ns['active_popups'] = active_popups

def add_geojson_to_map(geojson_data, map):
     # GeoJSON-Layer erstellen
    geo_json = GeoJSON(data=geojson_data, name='Route')
    fuel_list=calculate_cumulative_fuel(geo_json)
    # Klick-Event-Handler setzen
    geo_json.on_click(lambda event, feature, **kwargs: display_marker_popup(event, feature, map, fuel_list))
    
    # GeoJSON-Layer zur Karte hinzufügen
    map.add(geo_json)
    return geo_json