import json
from datetime import datetime, timedelta
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

global start_date 
start_date = datetime(2025, 4, 1, 9, 0)
global end_time
end_time = datetime(2025, 4, 5, 6, 0)


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
    global start_date 
    if route_displayed==False :
        a,b=marker1.location
        c,d=marker2.location
        slider_minutes = time_slider.value * 15
        selected_time = start_date + timedelta(minutes=slider_minutes)
        iso_time = selected_time.strftime("%Y-%m-%dT%H:%MZ")
        with open('config.template.json', 'r+') as f:
            data = json.load(f)
            data['DEFAULT_ROUTE'] = [a,b,c,d]
            data['DEPARTURE_TIME']=iso_time
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


start_time = datetime(2025, 4, 1, 9, 0)
end_time = datetime(2025, 4, 5, 6, 0)

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
    time_display.value = f"Aktuelle Zeit: {formatted_time}"

# Initiales Label setzen
update_time_display({'new': 0})

# Observer registrieren
time_slider.observe(update_time_display, names='value')

# Add callbacks for the buttons and display them and he map 
button1.on_click(on_button1_clicked)
button2.on_click(on_button2_clicked)
ui= widgets.HBox([widgets.VBox([time_slider, time_display]), button1, button2])
display(ui)
display(m, info_output)
