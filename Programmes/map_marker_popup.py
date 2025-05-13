from ipyleaflet import Marker, GeoJSON, Popup
from ipywidgets import HTML
from datetime import datetime

def add_cumulative_fuel_to_features(geojson_data):
    """
    Fügt jedem Feature im GeoJSON den kumulierten Treibstoffverbrauch als Attribut hinzu.
    """
    features = geojson_data.get('features', [])
    cumulative_fuel = 0.0

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

            cumulative_fuel += fuel_used
        except Exception as e:
            cumulative_fuel += 0.0  # im Fehlerfall keine Änderung

        curr['properties']['cumulative_fuel_used'] = cumulative_fuel

    # Zielpunkt bekommt kein validen Wert
    if features:
        features[-1]['properties']['cumulative_fuel_used'] = None

    return geojson_data


def display_marker_popup(event, feature, map):
    """
    Zeigt ein Popup mit Informationen zum angeklickten Punkt.
    """
    properties = feature.get('properties', {})
    coords = feature.get('geometry', {}).get('coordinates', [None, None])
    lat, lon = coords[1], coords[0]

    lines = []

    time = properties.get("time", "N/A")
    speed = properties.get("speed", {}).get("value", "N/A")
    fuel = properties.get("fuel_consumption", {}).get("value", "N/A")
    fuel_type = properties.get("fuel_type", "N/A")
    cumulative = properties.get("cumulative_fuel_used")

    lines.append(f"<b>Time:</b> {time}")
    lines.append(f"<b>Speed:</b> {speed} m/s")
    lines.append(f"<b>Fuel consumption:</b> {fuel} t/h")
    lines.append(f"<b>Fuel type:</b> {fuel_type}")

    if cumulative is not None:
        lines.append(f"<b>Cumulative fuel used:</b> {cumulative:.2f} t")
    else:
        lines.append(f"<b>Cumulative fuel used:</b> N/A")

    html = HTML("<br>".join(lines))
    popup = Popup(location=(lat, lon), child=html, close_button=True, auto_close=False)
    
    marker = Marker(location=(lat + 0.02, lon), opacity=0)
    marker.popup = popup

    map.add(marker)


def add_geojson_to_map(geojson_data, map):
    """
    Fügt GeoJSON-Daten zur Karte hinzu, berechnet den kumulierten Treibstoffverbrauch,
    und registriert einen Klick-Handler für Popups.
    """
    # Kumulierten Treibstoff berechnen
    geojson_data = add_cumulative_fuel_to_features(geojson_data)

    # Layer erstellen
    geo_json = GeoJSON(data=geojson_data, name='Route')
    geo_json.on_click(lambda event, feature, **kwargs: display_marker_popup(event, feature, map))

    # Zur Karte hinzufügen
    map.add(geo_json)
    return geo_json
