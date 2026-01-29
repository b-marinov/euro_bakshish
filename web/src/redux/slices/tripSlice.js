import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { tripService } from '../../services/services';

export const fetchMyTrips = createAsyncThunk(
  'trip/fetchMyTrips',
  async (_, { rejectWithValue }) => {
    try {
      const data = await tripService.getMyTrips();
      return data;
    } catch (error) {
      return rejectWithValue(error.response?.data);
    }
  }
);

export const fetchTripHistory = createAsyncThunk(
  'trip/fetchTripHistory',
  async (role = 'all', { rejectWithValue }) => {
    try {
      const data = await tripService.getTripHistory(role);
      return data;
    } catch (error) {
      return rejectWithValue(error.response?.data);
    }
  }
);

export const createTrip = createAsyncThunk(
  'trip/createTrip',
  async (tripData, { rejectWithValue }) => {
    try {
      const data = await tripService.createTrip(tripData);
      return data;
    } catch (error) {
      return rejectWithValue(error.response?.data);
    }
  }
);

const tripSlice = createSlice({
  name: 'trip',
  initialState: {
    activeTrips: [],
    tripHistory: [],
    loading: false,
    error: null,
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMyTrips.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchMyTrips.fulfilled, (state, action) => {
        state.loading = false;
        state.activeTrips = action.payload;
      })
      .addCase(fetchMyTrips.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchTripHistory.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchTripHistory.fulfilled, (state, action) => {
        state.loading = false;
        state.tripHistory = action.payload;
      })
      .addCase(fetchTripHistory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createTrip.pending, (state) => {
        state.loading = true;
      })
      .addCase(createTrip.fulfilled, (state, action) => {
        state.loading = false;
        state.activeTrips.push(action.payload);
      })
      .addCase(createTrip.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError } = tripSlice.actions;
export default tripSlice.reducer;
