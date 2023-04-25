import requests


def getArrivals(stop_code):
    res = requests.post(f"http://api.tfl.gov.uk/StopPoint/{stop_code}/Arrivals?app_id=BusBoard&app_key=8c7f656786344818b35db9f3f1e36e1e")
    arrivals = res.json()
    return arrivals