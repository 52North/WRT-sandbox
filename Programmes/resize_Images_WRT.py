import os
from PIL import Image

# Folder containing the original images
image_folder = "/home/jovyan/Graphics-WRT"
target_width = 600  # Target width in pixels

# Optionally: only process certain image types
valid_extensions = ('.png')

# Get all matching image files in the folder
image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith(valid_extensions)
]

# Raise an error if no valid image files are found
if not image_files:
    raise FileNotFoundError(f"No image files with extensions {valid_extensions} found in '{image_folder}'.")

for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    
    with Image.open(image_path) as img:
        # Skip image if it's already smaller than the target width
        if img.width <= target_width:
            continue
        
        # Calculate new height to maintain aspect ratio
        w_percent = target_width / float(img.width)
        new_height = int(float(img.height) * w_percent)

        # Resize image using high-quality resampling
        resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

        # Overwrite image and save with minimal quality loss
        resized_img.save(image_path, optimize=True)
