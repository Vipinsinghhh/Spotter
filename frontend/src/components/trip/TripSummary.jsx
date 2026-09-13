import { useSelector } from "react-redux";

function TripSummary() {
  const tripData = useSelector((state) => state.trip.tripData);

  if (!tripData) {
    return null;
  }

  const { route, hos_schedule } = tripData;

  return (
    <section>
      <h2>Trip Summary</h2>

      <div>
        <h3>Route</h3>

        <p>
          Distance: {route.distance_miles.toFixed(2)} miles
        </p>

        <p>
          Driving Time: {route.duration_hours.toFixed(2)} hours
        </p>
      </div>

      <div>
        <h3>HOS</h3>

        <p>
          Cycle Remaining:{" "}
          {hos_schedule.cycle_remaining_hours.toFixed(2)} hours
        </p>

        <p>
          Fuel Stops: {hos_schedule.fuel_stops}
        </p>

        <p>
          Total Driving:{" "}
          {hos_schedule.total_driving_hours.toFixed(2)} hours
        </p>
      </div>

      <div>
        <h3>Days</h3>

        {hos_schedule.days.map((day) => (
          <div key={day.day}>
            <h4>Day {day.day}</h4>

            <p>
              Driving: {day.driving_hours.toFixed(2)} hours
            </p>

            <p>
              On Duty: {day.on_duty_hours?.toFixed(2) ?? 0} hours
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default TripSummary;