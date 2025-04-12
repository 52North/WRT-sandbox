import os
from PIL import Image

# Ordner mit Originalbildern
image_folder = "Images-WRT"
target_width = 600  # Zielbreite in Pixeln

# Optional: Nur bestimmte Bildtypen
valid_extensions = ('.png')

# Alle passenden Bilddateien holen
image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith(valid_extensions)
]

for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    
    with Image.open(image_path) as img:
        # Falls Bild schon kleiner ist, überspringen
        if img.width <= target_width:
            continue
        
        # Neue Höhe berechnen (Seitenverhältnis beibehalten)
        w_percent = target_width / float(img.width)
        new_height = int(float(img.height) * w_percent)

        # Bild verkleinern mit hochwertigem Filter
        resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

        # Überschreiben, möglichst verlustarm speichern
        if filename.lower().endswith(('.jpg', '.jpeg')):
            resized_img.save(image_path, format='JPEG', quality=95, optimize=True)
        else:
            resized_img.save(image_path, optimize=True)
        