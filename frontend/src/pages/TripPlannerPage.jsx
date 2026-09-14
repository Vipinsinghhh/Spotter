import TripForm from "../components/trip/TripForm";
import TripSummary from "../components/trip/TripSummary";
import TripMap from "../components/map/TripMap";

function TripPlannerPage() {
  return (
    <main>
      <h1>Spotter Trip Planner</h1>

      <TripForm />

      <TripSummary />

      <TripMap />
    </main>
  );
}

export default TripPlannerPage;