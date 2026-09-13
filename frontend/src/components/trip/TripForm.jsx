import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import Input from "../common/Input";
import { planTrip } from "../../features/trip/tripSlice";

function TripForm() {
  const dispatch = useDispatch();

  const { loading, error } = useSelector(
    (state) => state.trip
  );

  const [formData, setFormData] = useState({
    currentLocation: "",
    pickupLocation: "",
    dropoffLocation: "",
    cycleUsedHours: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    dispatch(
      planTrip({
        current_location: formData.currentLocation,
        pickup_location: formData.pickupLocation,
        dropoff_location: formData.dropoffLocation,
        cycle_used_hours: Number(formData.cycleUsedHours),
      })
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Current Location"
        name="currentLocation"
        placeholder="Enter current location"
        value={formData.currentLocation}
        onChange={handleChange}
      />

      <Input
        label="Pickup Location"
        name="pickupLocation"
        placeholder="Enter pickup location"
        value={formData.pickupLocation}
        onChange={handleChange}
      />

      <Input
        label="Dropoff Location"
        name="dropoffLocation"
        placeholder="Enter dropoff location"
        value={formData.dropoffLocation}
        onChange={handleChange}
      />

      <Input
        label="Cycle Used Hours"
        name="cycleUsedHours"
        type="number"
        placeholder="Enter cycle used hours"
        value={formData.cycleUsedHours}
        onChange={handleChange}
      />

      <button
        type="submit"
        disabled={loading}
      >
        {loading ? "Planning Trip..." : "Plan Trip"}
      </button>

      {error && (
        <p>
          {typeof error === "string"
            ? error
            : "Failed to plan trip"}
        </p>
      )}
    </form>
  );
}

export default TripForm;