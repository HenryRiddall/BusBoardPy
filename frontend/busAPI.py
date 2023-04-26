import requests


def get_stop_points(postcode=""):
    res = requests.post("http://127.0.0.1:5000/stop_points", data={"postcode": postcode})
    if res.ok:
        response = res.json()
        if "stop_points" in response:
            return response["stop_points"]
        return []
    
    return {}