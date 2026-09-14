import { Marker, Popup } from "react-leaflet";

function MapMarker({ position, title, description }) {
  return (
    <Marker position={position}>
      <Popup>
        <strong>{title}</strong>

        {description && <p>{description}</p>}
      </Popup>
    </Marker>
  );
}

export default MapMarker;