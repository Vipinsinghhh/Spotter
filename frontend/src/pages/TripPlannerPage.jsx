import TripForm from "../components/trip/TripForm";
import TripSummary from "../components/trip/TripSummary";

function TripPlannerPage() {
  return (
    <main>
      <h1>Spotter Trip Planner</h1>

      <TripForm />

      <TripSummary />
    </main>
  );
}

export default TripPlannerPage;