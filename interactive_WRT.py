import json
import datetime
import os
import subprocess
from ipyleaflet import Map, Marker, AwesomeIcon, GeoJSON
import ipywidgets as widgets
from ipywidgets import Button
from IPython.display import display

# Define the look of the map markers
icon1 = AwesomeIcon(
    name='map-pin',       
    marker_color='green',       
    icon_color='white',       
    spin=False
)

icon2 = AwesomeIcon(
    name='map-pin',       
    marker_color='red',       
    icon_color='white',       
    spin=False
)

# Define the map and the map markers
center = ([39.926688, 7.930542])
m = Map(center=center, zoom=6)
marker1 = Marker(location=([39.926688, 5]), draggable=True, icon=icon1)
marker2 = Marker(location=([39.926688, 10.5]), draggable=True, icon=icon2)
m.add(marker1)
m.add(marker2)

# Define Buttons to start the routing and to set a new route
button1= widgets.Button(description="start routing")
button2= widgets.Button(description="new route")

# Set variable route_displayed as false
global route_displayed
route_displayed = False

# define output for geojson data
info_output = widgets.Output()

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

# Function that deletes the last route and sets the map markers to their default position
def on_button2_clicked(b):
    global route_displayed
    if route_displayed==True:
        marker1.location=(39.926688, 5)
        marker2.location=(39.926688, 10.5)
        m.remove(geo_json)
        m.add(marker1)
        m.add(marker2)
        route_displayed=False
    else:
        print("Map markers already in default position")


# Function thet rewrites the config file so the WRT calculates the route between the given map markers,
# starts the WRT and displays the calculated route
def on_button1_clicked(b):
    global route_displayed
    if route_displayed==False :
        a,b=marker1.location
        c,d=marker2.location
        with open('config.template.json', 'r+') as f:
            data = json.load(f)
            data['DEFAULT_ROUTE'] = [a,b,c,d]
        with open('config.template.json', 'w') as file: 
            json.dump(data, file, indent=4)
        subprocess.run(["python", "delete_Images_WRT.py"])
        subprocess.run(["python", "cli.py", "-f", "config.template.json"])
        with open("min_time_route.json") as f:
            data = json.load(f)
        global geo_json
        geo_json = GeoJSON(data=data)
        geo_json.on_click(handle_click)
        m.remove(marker1)
        m.remove(marker2)
        m.add(geo_json) 
        route_displayed=True 
    else:
        print("Route already displayed")


# Funktion zum Umrechnen eines Sliderwerts in eine Zeit
def slider_value_to_time(value):
    minutes = value * 15
    return f"{minutes // 60:02d}:{minutes % 60:02d}"

# Initialer Zeitwert
initial_value = 0
initial_time = slider_value_to_time(initial_value)

# Slider-Widget mit leerer Beschreibung (diese wird dynamisch gesetzt)
time_slider = widgets.IntSlider(
    value=initial_value,
    min=0,
    max=95,
    step=1,
    description=f"Uhrzeit: {initial_time}",
    continuous_update=True,
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='500px')
)

# Callback zur Aktualisierung der Beschriftung
def update_description(change):
    new_time = slider_value_to_time(change['new'])
    time_slider.description = f"Uhrzeit: {new_time}"

# Verbindung Slider ↔ Callback
time_slider.observe(update_description, names='value')


# Add callbacks for the buttons and display them and he map 
button1.on_click(on_button1_clicked)
button2.on_click(on_button2_clicked)
ui= widgets.HBox([button1, button2])
display(ui)
display(m, info_output)
display(time_slider)