import { configureStore } from "@reduxjs/toolkit";
import tripReducer from "../features/trip/tripSlice";

export const store = configureStore({
  reducer: {
    trip: tripReducer,
  },
});