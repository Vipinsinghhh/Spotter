import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import tripService from "../../services/tripService";

export const planTrip = createAsyncThunk(
  "trip/planTrip",
  async (tripData, { rejectWithValue }) => {
    try {
      const data = await tripService.planTrip(tripData);

      return data;
    } catch (error) {
      return rejectWithValue(
        error.response?.data || "Something went wrong"
      );
    }
  }
);

const initialState = {
  tripData: null,
  loading: false,
  error: null,
};

const tripSlice = createSlice({
  name: "trip",
  initialState,

  reducers: {
    clearTrip: (state) => {
      state.tripData = null;
      state.error = null;
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(planTrip.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(planTrip.fulfilled, (state, action) => {
        state.loading = false;
        state.tripData = action.payload;
      })

      .addCase(planTrip.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearTrip } = tripSlice.actions;

export default tripSlice.reducer;