from ipyleaflet import GeoJSON, Popup
from ipywidgets import HTML
from datetime import datetime

# Hilfsfunktion zum Parsen von Zeitstempeln
def parse_iso8601(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%MZ")
    except:
        return None

# Verbrauch bis zu einem bestimmten Index berechnen
def get_cumulative_fuel_used(geojson_data, to_index):
    features = geojson_data.get("features", [])
    if to_index <= 0 or to_index >= len(features):
        return 0.0

    total_fuel = 0.0
    for i in range(1, to_index + 1):
        f_prev = features[i - 1]
        f_curr = features[i]

        t0 = parse_iso8601(f_prev.get("properties", {}).get("time", ""))
        t1 = parse_iso8601(f_curr.get("properties", {}).get("time", ""))
        rate = f_prev.get("properties", {}).get("fuel_consumption", {}).get("value", None)

        if t0 and t1 and isinstance(rate, (int, float)):
            delta_h = (t1 - t0).total_seconds() / 3600.0
            total_fuel += rate * delta_h

    return round(total_fuel, 3)

# Popup-Anzeige bei Marker-Klick
def display_marker_popup(event, feature, map, geojson_data):
    props = feature['properties']
    coordinates = feature['geometry']['coordinates'][::-1]
    coordinates[0] += 0.45  # vertikal verschieben

    time_text = props.get("time", {})
    fuel = props.get("fuel_consumption", {})
    speed = props.get("speed", {})
    power = props.get("engine_power", {})

    index = props.get("_index", None)
    if index is not None:
        fuel_used = get_cumulative_fuel_used(geojson_data, index)
        fuel_used_text = f"{fuel_used} t"
    else:
        fuel_used_text = "?"

    popup_content = HTML()
    popup_content.value = f"""
        <b>Time:</b> {time_text}<br>
        <b>Fuel consumption:</b> {fuel.get('value', '–')} {fuel.get('unit', '')}<br>
        <b>Speed:</b> {speed.get('value', '–')} {speed.get('unit', '')}<br>
        <b>Engine power:</b> {power.get('value', '–')} {power.get('unit', '')}<br>
        <b>Cumulative fuel used:</b> {fuel_used_text}
    """

    popup = Popup(
        location=coordinates,
        child=popup_content,
        close_button=True,
        auto_close=False,
        close_on_escape_key=True
    )
    map.add(popup)

# GeoJSON zur Karte hinzufügen und Klick-Events registrieren
def add_geojson_to_map(geojson_data, map):
    features = geojson_data.get("features", [])
    for i, f in enumerate(features):
        f.setdefault("properties", {})["_index"] = i

    geo_json = GeoJSON(data=geojson_data, name='Route')

    # Event mit Übergabe von geojson_data
    geo_json.on_click(lambda event, feature, **kwargs: display_marker_popup(event, feature, map, geojson_data))

    map.add(geo_json)
    return geo_json
