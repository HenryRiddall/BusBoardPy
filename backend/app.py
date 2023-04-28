from flask import Flask, request
import requests
import urllib

app = Flask(__name__)

app_id = "BusBoard"
app_key = "8c7f656786344818b35db9f3f1e36e1e"


@app.route('/stop_points', methods=["POST"])
def get_arrivals():
    postcode = request.form.get("postcode")
    
    if not postcode:
        return {}
    
    lat, long = postcode_to_lat_long(postcode)
    
    stop_points = lat_long_to_stop_points(lat, long)
    
    [update_arrivals(stop_point) for stop_point in stop_points]
    
    return {"stop_points": stop_points}


def postcode_to_lat_long(postcode):
    api_url = f"https://api.postcodes.io/postcodes/{postcode}"
    
    api_response = requests.get(api_url)
    
    if not api_response.ok:
        return {}
    
    response_data = api_response.json()["result"]
    
    lat = response_data["latitude"]
    long = response_data["longitude"]
    
    return (lat, long)

def lat_long_to_stop_points(lat, long):
    api_url = f"https://api.tfl.gov.uk/StopPoint/?radius=250&lat={lat}&lon={long}&stopTypes=NaptanPublicBusCoachTram&app_id={app_id}&app_key={app_key}"
    
    api_response = requests.get(api_url)
    
    if not api_response.ok:
        return {}
    
    response_data = api_response.json()["stopPoints"]
    
    stop_points = [{"id": d['naptanId'], "name": d['commonName'], "indicator": d['indicator'], "arrivals": []} for d in response_data]
    
    stop_points.append({"id": "syke", "name": "TEST STOP", "indicator": "uhhh", "arrivals": []})
    
    return stop_points

def update_arrivals(stop_point):
    stop_id = stop_point["id"]
    api_url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}/Arrivals?app_id={app_id}&app_key={app_key}"
    
    api_response = requests.get(api_url)
    
    if not api_response.ok:
        return {}
    
    response_data = api_response.json()
    
    arrivals = [format_arrival(arrival) for arrival in response_data]
    
    
    arrivals = sorted(arrivals, key=lambda arrival: arrival['time_to_station'])
    
    stop_point["arrivals"] = arrivals
    
    return stop_point
    
def format_arrival(arrival):
    formatted_arrival = {
        "number": arrival["lineName"],
        "destination": arrival["destinationName"],
        "time_to_station": divmod(arrival["timeToStation"], 60)
    }
    
    return formatted_arrival