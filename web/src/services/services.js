import api from './api';

export const authService = {
  login: async (username, password) => {
    const response = await api.post('/users/token/', { username, password });
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me/');
    return response.data;
  },

  updateProfile: async (profileData) => {
    const response = await api.put('/users/update_profile/', profileData);
    return response.data;
  },
};

export const tripService = {
  createTrip: async (tripData) => {
    const response = await api.post('/trips/', tripData);
    return response.data;
  },

  getMyTrips: async () => {
    const response = await api.get('/trips/my_trips/');
    return response.data;
  },

  getTripHistory: async (role = 'all') => {
    const response = await api.get(`/trips/trip_history/?role=${role}`);
    return response.data;
  },

  getPendingTrips: async () => {
    const response = await api.get('/trips/pending_trips/');
    return response.data;
  },

  acceptTrip: async (tripId) => {
    const response = await api.post(`/trips/${tripId}/accept/`);
    return response.data;
  },

  startTrip: async (tripId) => {
    const response = await api.post(`/trips/${tripId}/start/`);
    return response.data;
  },

  completeTrip: async (tripId) => {
    const response = await api.post(`/trips/${tripId}/complete/`);
    return response.data;
  },

  cancelTrip: async (tripId) => {
    const response = await api.post(`/trips/${tripId}/cancel/`);
    return response.data;
  },
};

export const ratingService = {
  createReview: async (reviewData) => {
    const response = await api.post('/ratings/reviews/', reviewData);
    return response.data;
  },

  getMyReviewsReceived: async () => {
    const response = await api.get('/ratings/reviews/my_reviews_received/');
    return response.data;
  },

  getMyReviewsGiven: async () => {
    const response = await api.get('/ratings/reviews/my_reviews_given/');
    return response.data;
  },

  getPendingReviews: async () => {
    const response = await api.get('/ratings/reviews/pending_reviews/');
    return response.data;
  },

  getUserSummary: async (userId) => {
    const response = await api.get(`/ratings/reviews/user_summary/?user_id=${userId}`);
    return response.data;
  },
};
