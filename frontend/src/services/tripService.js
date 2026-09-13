import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const tripService = {
  planTrip: async (tripData) => {
    const response = await axios.post(
      `${API_URL}/plan-trip/`,
      tripData
    );

    return response.data;
  },
};

export default tripService;