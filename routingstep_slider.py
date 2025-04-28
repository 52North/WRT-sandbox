import os
import re
import subprocess
from PIL import Image
from IPython.display import display, clear_output
import ipywidgets as widgets

if not os.listdir("Images-WRT"):
    raise RuntimeError("Image folder empty")

# Resize images
subprocess.run(["python", "resize_Images_WRT.py"])

# Define key for sorted function
def natural_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


# Set path to Images folder
image_folder = "Images-WRT"
image_files = sorted([
    f for f in os.listdir(image_folder)
    if f.lower().startswith('fig') and f.lower().endswith('.png')
    ], key=natural_key)

# Output-Widget for the image 
image_output = widgets.Output()

# Function for displaying the images
def show_image(index):
    image_path = os.path.join(image_folder, image_files[index])
    with image_output:
        image_output.clear_output(wait=True)
        img = Image.open(image_path)
        display(img)

# Defining the slider
slider = widgets.IntSlider(
    value=0,
    min=0,
    max=len(image_files) - 1,
    step=1,
    orientation='vertical',
    description='routing-step',
    continuous_update=True,
    layout=widgets.Layout(height='300px')
)

# Callback for the slider
slider.observe(lambda change: show_image(change['new']), names='value')

# Layout
ui = widgets.HBox([slider,image_output], layout=widgets.Layout(align_items='center'))

# Show first image
show_image(0)

# Show ui
display(ui)