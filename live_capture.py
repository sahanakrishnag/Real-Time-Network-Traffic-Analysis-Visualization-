from scapy.all import rdpcap, IP
import folium
import requests

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            lat = data["lat"]
            lon = data["lon"]
            country = data["country"]
            org = data.get("org", "Unknown")
            return lat, lon, f"{org}, {country}"
    except:
        pass
    return 0, 0, "Unknown"

def process_pcap(pcap_path, output_map="templates/map.html"):
    packets = rdpcap(pcap_path)
    ip_traffic = {}

    for pkt in packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            ip_traffic[(src, dst)] = ip_traffic.get((src, dst), 0) + 1

    # Create folium map centered on global view
    fmap = folium.Map(location=[20, 0], zoom_start=2)
    coords_map = {}

    for (src, dst), count in ip_traffic.items():
        if src not in coords_map:
            coords_map[src] = get_location(src)
        if dst not in coords_map:
            coords_map[dst] = get_location(dst)

        src_lat, src_lon, src_info = coords_map[src]
        dst_lat, dst_lon, dst_info = coords_map[dst]

        # Add markers
        folium.Marker(
            location=[src_lat, src_lon],
            popup=f"{src} ({src_info})",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(fmap)

        folium.Marker(
            location=[dst_lat, dst_lon],
            popup=f"{dst} ({dst_info})",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(fmap)

        # Draw line
        folium.PolyLine(
            locations=[[src_lat, src_lon], [dst_lat, dst_lon]],
            tooltip=f"{src} ➝ {dst} ({count} packets)",
            color="red"
        ).add_to(fmap)

    # Save to HTML
    fmap.save(output_map)
