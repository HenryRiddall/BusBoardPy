import requests


def get_stop_points(postcode=""):
    res = requests.post("http://127.0.0.1:5000/stop_points", data={"postcode": postcode})
    if res.ok:
        response = res.json()
        return response["stop_points"]
    
    return {}