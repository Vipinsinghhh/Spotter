import requests
import time


DRIVING_LIMIT_HOURS = 11
ON_DUTY_WINDOW_HOURS = 14
BREAK_AFTER_DRIVING_HOURS = 8
CYCLE_LIMIT_HOURS = 70
FUEL_STOP_MILES = 1000
PICKUP_TIME_HOURS = 1
DROPOFF_TIME_HOURS = 1


def calculate_available_hours(cycle_used_hours):
    cycle_remaining = CYCLE_LIMIT_HOURS - cycle_used_hours

    return {
        "cycle_remaining_hours": cycle_remaining,
        "driving_limit_hours": DRIVING_LIMIT_HOURS,
        "on_duty_window_hours": ON_DUTY_WINDOW_HOURS,
    }


def geocode_location(location):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "jsonv2",
        "limit": 1,
    }

    headers = {
        "User-Agent": "SpotterAI/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    results = response.json()

    if not results:
        return None

    return {
        "latitude": float(results[0]["lat"]),
        "longitude": float(results[0]["lon"]),
        "display_name": results[0]["display_name"],
    }


def geocode_trip_locations(current_location, pickup_location, dropoff_location):
    current = geocode_location(current_location)

    time.sleep(1)

    pickup = geocode_location(pickup_location)

    time.sleep(1)

    dropoff = geocode_location(dropoff_location)

    return {
        "current_location": current,
        "pickup_location": pickup,
        "dropoff_location": dropoff,
    }

   