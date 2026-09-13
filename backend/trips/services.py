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

def get_route(locations):
    coordinates = ";".join(
        f"{location['longitude']},{location['latitude']}"
        for location in locations
    )

    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data["code"] != "Ok":
        return None

    route = data["routes"][0]

    return {
    "distance_miles": route["distance"] / 1609.34,
    "duration_hours": route["duration"] / 3600,
    "geometry": route["geometry"],
    "legs": [
        {
            "distance_miles": leg["distance"] / 1609.34,
            "duration_hours": leg["duration"] / 3600,
        }
        for leg in route["legs"]
    ],
}
    
def calculate_hos_schedule(
    duration_hours,
    cycle_used_hours,
    distance_miles,
):
    cycle_remaining = CYCLE_LIMIT_HOURS - cycle_used_hours

    average_speed = distance_miles / duration_hours

    days = []
    remaining_driving = duration_hours

    day_number = 1
    total_distance_driven = 0
    next_fuel_mile = FUEL_STOP_MILES

    trip_started = False

    while remaining_driving > 0:

        # 34-hour restart if cycle is exhausted
        if cycle_remaining <= 0:
            days.append({
                "day": day_number,
                "driving_hours": 0,
                "events": [
                    {
                        "type": "restart",
                        "duration_hours": 34,
                    }
                ],
                "cycle_remaining_before_restart": 0,
            })

            cycle_remaining = CYCLE_LIMIT_HOURS
            day_number += 1

            continue

        events = []

        on_duty_hours = 0
        driving_today = 0
        driving_since_break = 0

        # Pickup only when trip actually starts
        if not trip_started:
            events.append({
                "type": "pickup",
                "duration_hours": PICKUP_TIME_HOURS,
            })

            on_duty_hours += PICKUP_TIME_HOURS
            cycle_remaining -= PICKUP_TIME_HOURS
            trip_started = True

        while (
            remaining_driving > 0
            and driving_today < DRIVING_LIMIT_HOURS
            and on_duty_hours < ON_DUTY_WINDOW_HOURS
            and cycle_remaining > 0
        ):

            # Take break after 8 hours of cumulative driving
            if driving_since_break >= BREAK_AFTER_DRIVING_HOURS:
                events.append({
                    "type": "break",
                    "duration_hours": 0.5,
                })

                driving_since_break = 0
                continue

            # Distance until next fuel stop
            distance_until_fuel = (
                next_fuel_mile - total_distance_driven
            )

            driving_until_fuel = (
                distance_until_fuel / average_speed
            )

            driving_until_break = (
                BREAK_AFTER_DRIVING_HOURS
                - driving_since_break
            )

            available_driving = min(
                remaining_driving,
                DRIVING_LIMIT_HOURS - driving_today,
                ON_DUTY_WINDOW_HOURS - on_duty_hours,
                cycle_remaining,
                driving_until_fuel,
                driving_until_break,
            )

            if available_driving <= 0:
                break

            events.append({
                "type": "driving",
                "duration_hours": round(available_driving, 2),
            })

            remaining_driving -= available_driving
            driving_today += available_driving
            driving_since_break += available_driving
            on_duty_hours += available_driving
            cycle_remaining -= available_driving

            total_distance_driven += (
                available_driving * average_speed
            )

            # Fuel stop at 1000-mile intervals
            if (
                total_distance_driven >= next_fuel_mile
                and next_fuel_mile <= distance_miles
            ):
                if on_duty_hours + 0.5 <= ON_DUTY_WINDOW_HOURS:
                    events.append({
                        "type": "fuel",
                        "duration_hours": 0.5,
                        "at_mile": round(next_fuel_mile, 2),
                    })

                    on_duty_hours += 0.5
                    cycle_remaining -= 0.5
                    next_fuel_mile += FUEL_STOP_MILES
                else:
                    break

        # Dropoff when all driving is completed
        if remaining_driving <= 0:
            if on_duty_hours + DROPOFF_TIME_HOURS <= ON_DUTY_WINDOW_HOURS:
                events.append({
                    "type": "dropoff",
                    "duration_hours": DROPOFF_TIME_HOURS,
                })

                on_duty_hours += DROPOFF_TIME_HOURS
                cycle_remaining -= DROPOFF_TIME_HOURS

        days.append({
            "day": day_number,
            "driving_hours": round(driving_today, 2),
            "on_duty_hours": round(on_duty_hours, 2),
            "on_duty_window_hours": ON_DUTY_WINDOW_HOURS,
            "cycle_remaining_hours": round(
                max(cycle_remaining, 0),
                2,
            ),
            "events": events,
        })

        day_number += 1

    return {
        "total_driving_hours": round(duration_hours, 2),
        "total_distance_miles": round(distance_miles, 2),
        "cycle_remaining_hours": round(
            max(cycle_remaining, 0),
            2,
        ),
        "days": days,
    }
    
def generate_daily_logs(hos_schedule):
    daily_logs = []

    for day in hos_schedule["days"]:
        current_hour = 0
        segments = []

        for event in day["events"]:
            duration = event["duration_hours"]

            segments.append({
                "type": event["type"],
                "start_hour": round(current_hour, 2),
                "end_hour": round(current_hour + duration, 2),
                "duration_hours": duration,
            })

            current_hour += duration

        # Remaining time of the 24-hour day is off duty
        if current_hour < 24:
            segments.append({
                "type": "off_duty",
                "start_hour": round(current_hour, 2),
                "end_hour": 24,
                "duration_hours": round(24 - current_hour, 2),
            })

        daily_logs.append({
            "day": day["day"],
            "segments": segments,
        })

    return daily_logs    