import requests
import time

from django.http import HttpResponseForbidden


def get_driving_distance(origin, destination, api_key):
    """
    Get the driving distance between two addresses using Google Distance Matrix API.
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": origin,
        "destinations": destination,
        "units": "imperial",
        "mode": "driving",  # Options: driving, walking, bicycling, transit
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        try:
            distance_text = data["rows"][0]["elements"][0]["distance"]["text"]  # e.g., "45.2 miles"
            distance_text = distance_text.replace(" mi", " miles")
            duration_text = data["rows"][0]["elements"][0]["duration"]["text"]  # e.g., "1 hour 10 mins"
            return {
                "distance_text": distance_text,
                "duration_text": duration_text
            }
        except (KeyError, IndexError):
            return None

    return None


def check_for_spam(request):
    # 1. Honeypot check
    if request.POST.get('middle_name'):
        return HttpResponseForbidden('Spam detected (honeypot filled)')

    if request.POST.get('name') == 'RobertGurse':
        return HttpResponseForbidden('Spam detected (forbidden name)')
