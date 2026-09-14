import {
  MapContainer,
  TileLayer,
  Polyline,
} from "react-leaflet";

import { useSelector } from "react-redux";

import "leaflet/dist/leaflet.css";

function TripMap() {
  const tripData = useSelector(
    (state) => state.trip.tripData
  );

  const geometry =
    tripData?.route?.geometry?.coordinates || [];

  // OSRM coordinates are [longitude, latitude]
  // Leaflet expects [latitude, longitude]
  const routeCoordinates = geometry.map(
    ([longitude, latitude]) => [
      latitude,
      longitude,
    ]
  );

  return (
    <MapContainer
      center={[39.5, -98.35]}
      zoom={4}
      style={{
        height: "500px",
        width: "100%",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {routeCoordinates.length > 0 && (
        <Polyline positions={routeCoordinates} />
      )}
    </MapContainer>
  );
}

export default TripMap;