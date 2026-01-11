import folium
from geopy.geocoders import Nominatim

def process_pcap(pcap_path):
    print(f"Processing: {pcap_path}")

    # Dummy coordinates for example — replace with parsed IP geolocation
    coords = [(37.7749, -122.4194), (40.7128, -74.0060)]  # SF to NYC

    # Create a map
    fmap = folium.Map(location=coords[0], zoom_start=5)
    for lat, lon in coords:
        folium.Marker(location=(lat, lon)).add_to(fmap)

    # Draw a line between points
    folium.PolyLine(coords, color="red").add_to(fmap)

    # Save to templates/map.html
    fmap.save("templates/map.html")

    return coords
