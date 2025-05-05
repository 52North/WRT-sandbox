import json
from datetime import datetime, timedelta
import os
import subprocess
from ipyleaflet import Map, Marker, AwesomeIcon, GeoJSON, Rectangle
import ipywidgets as widgets
from ipywidgets import Button
from IPython.display import display
from map_marker_popup import add_geojson_to_map

subprocess.run(["python", "load_env.py"])

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

# Bounding box for weather data
bounds = [(37.0, 1.0), ( 42.0, 15.0)]
rect = Rectangle(
    bounds=bounds,
    color="green",
    fill_color="green",
    fill_opacity=0.2
)  
m.add(rect)
# Define Buttons to start the routing and to set a new route
button1= widgets.Button(description="start routing")
button2= widgets.Button(description="new route")

# Set variable route_displayed as false
global route_displayed
route_displayed = False

global geo_json
geo_json = None
global start_time 
start_time = datetime(2025, 4, 1, 9, 0)
global end_time
end_time = datetime(2025, 4, 5, 6, 0)


# define output for geojson data
info_output = widgets.Output()

# Function that deletes the last route and sets the map markers to their default position
def on_button2_clicked(b):
    global route_displayed
    global geo_json
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
    global start_date
    global geo_json 

    if route_displayed == False:
        a, b = marker1.location
        c, d = marker2.location
        slider_minutes = time_slider.value * 15
        selected_time = start_time + timedelta(minutes=slider_minutes)
        iso_time = selected_time.strftime("%Y-%m-%dT%H:%MZ")

        # Update config
        with open('/home/jovyan/Configuration/config.template.json', 'r+') as f:
            data = json.load(f)
            data['DEFAULT_ROUTE'] = [a, b, c, d]
            data['DEPARTURE_TIME'] = iso_time

        with open('/home/jovyan/Configuration/config.template.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Run subprocesses
        subprocess.run(["python", "delete_Images_WRT.py"])
        subprocess.run(["python", "cli.py", "-f", "/home/jovyan/Configuration/config.template.json"])

        # Read and display route
        with open("/home/jovyan/Data/min_time_route.json") as f:
            geodata = json.load(f)

        geo_layer = add_geojson_to_map(geodata, m)
        m.remove(marker1)
        m.remove(marker2)

        # Set global state
        route_displayed = True
        global geo_json
        geo_json = geo_layer
    else:
        print("Route already displayed")

# Anzahl der 15-Minuten-Schritte
step = timedelta(minutes=15)
total_steps = int((end_time - start_time) / step)

# Ausgabe-Widget
time_display = widgets.Label()

# Slider definieren
time_slider = widgets.IntSlider(
    value=0,
    min=0,
    max=total_steps,
    step=1,
    description='',
    continuous_update=True,
    readout = False,
    layout=widgets.Layout(width='600px')
)

# Callback zur Aktualisierung der Anzeige
def update_time_display(change):
    current_time = start_time + step * change['new']
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%MZ")
    time_display.value = f"Start time: {formatted_time}"

# Initiales Label setzen
update_time_display({'new': 0})

# Observer registrieren
time_slider.observe(update_time_display, names='value')

# Add callbacks for the buttons and display them and he map 
button1.on_click(on_button1_clicked)
button2.on_click(on_button2_clicked)
ui= widgets.HBox([widgets.VBox([time_slider, time_display]), widgets.VBox([button1, button2])])
display(ui)
display(m, info_output)
