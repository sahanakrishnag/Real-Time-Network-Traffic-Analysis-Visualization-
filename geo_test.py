import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
ip = "8.8.8.8"  # Google DNS
resp = reader.city(ip)
print(resp.location.latitude, resp.location.longitude)

