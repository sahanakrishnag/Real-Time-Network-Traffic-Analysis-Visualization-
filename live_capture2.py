import subprocess
import json
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def get_location(ip):
    try:
        response = reader.city(ip)
        return {"lat": response.location.latitude, "lon": response.location.longitude}
    except:
        return None

def capture_packets():
    tshark_cmd = ["tshark", "-T", "json", "-l", "-c", "30", "-f", "ip", "-e", "ip.src", "-e", "ip.dst"]
    process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    ip_data = []

    for line in process.stdout:
        try:
            data = json.loads(line)
            for pkt in data:
                src = pkt['_source']['layers'].get('ip.src')
                dst = pkt['_source']['layers'].get('ip.dst')
                if src and dst:
                    for ip in [src[0], dst[0]]:
                        if ip not in [i['ip'] for i in ip_data]:
                            location = get_location(ip)
                            if location:
                                ip_data.append({"ip": ip, "lat": location["lat"], "lon": location["lon"]})
        except:
            continue

        if len(ip_data) >= 10:
            break

    return ip_data

