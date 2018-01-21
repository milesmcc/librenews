from datetime import datetime

import pytz

import humanize
import pycountry
from geoip import geolite2

requests = 0
ips = []
starttime = datetime.now(pytz.UTC)
countries = {}
countries_total = 0


def request(ip_string):
    global requests, ips, countries, countries_total
    requests += 1
    if ip_string not in ips:
        ips.append(ip_string)
    match = geolite2.lookup(ip_string)
    if match:
        country = pycountry.countries.get(alpha_2=match.country).name
        if country in countries:
            countries[country] += 1
        else:
            countries[country] = 1
        countries_total += 1
        return match.continent + "/" + country + " - " + ip_string
    else:
        return "? - " + ip_string
    return "?!"


def unique_devices():  # give or take
    return len(ips)


def time():
    return humanize.naturaltime(datetime.now(pytz.UTC) - starttime)


def requests_per_second():
    return (requests + 0.0) / (datetime.now(pytz.UTC) - starttime).total_seconds()


def top_countries():
    ordered = sorted(countries, reverse=True, key=lambda k: countries[k])[:10]
    by_share = [(country, str((countries[country] * 100)/countries_total) + "%")
                for country in ordered]
    return by_share
