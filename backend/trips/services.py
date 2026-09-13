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