from geoip import geolite2
from datetime import datetime
import pytz
import humanize

requests = 0
ips = []
starttime = datetime.now(pytz.UTC)

def request(ip_string):
    global requests, ips
    requests += 1
    if ip_string not in ips:
        ips.append(ip_string)
    match = geolite2.lookup(ip_string)
    if match:
        return match.continent + "/" + match.country + " - " + ip_string
    else:
        return "? - " + ip_string

def unique_devices(): # give or take
    return len(ips)

def time():
    return humanize.naturaltime(datetime.now(pytz.UTC) - starttime)

def requests_per_second():
    return (requests + 0.0) / (datetime.now(pytz.UTC) - starttime).total_seconds()
