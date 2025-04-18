import json
import os
import subprocess
from ipyleaflet import Map, Marker, AwesomeIcon, GeoJSON
import ipywidgets as widgets
from ipywidgets import Button

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
        subprocess.run(["python", "cli.py -f config.template.json"])
        with open("min_time_route.json") as f:
            data = json.load(f)
        global geo_json
        geo_json = GeoJSON(data=data)
        m.remove(marker1)
        m.remove(marker2)
        m.add(geo_json) 
        route_displayed=True 
    else:
        print("Route already displayed")

# Add callbacks for the buttons and display them and he map 
button1.on_click(on_button1_clicked)
button2.on_click(on_button2_clicked)
ui= widgets.HBox([button1, button2])
display(ui)
m