import pyshark
import geoip2.database

def process_pcap(C:\Users\User\Documents\sample.pcapng):
    reader = geoip2.database.Reader("GeoLite2-City.mmdb")  # Make sure this file exists
    ip_locations = []

    try:
        capture = pyshark.FileCapture(filepath, display_filter='ip')

        seen_ips = set()
        for packet in capture:
            try:
                ip = packet.ip.src
                if ip not in seen_ips:
                    seen_ips.add(ip)

                    # Skip local/private IPs
                    if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172.") or ip == "127.0.0.1":
                        continue

                    response = reader.city(ip)
                    lat = response.location.latitude
                    lon = response.location.longitude

                    ip_locations.append({
                        "ip": ip,
                        "lat": lat,
                        "lon": lon
                    })
            except Exception:
                continue
        capture.close()
    except Exception as e:
        print(f"Error while processing pcap: {e}")

    return ip_locations

