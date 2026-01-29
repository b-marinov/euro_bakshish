import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, Paper, Grid, Card, CardContent } from '@mui/material';
import { fetchMyTrips } from '../redux/slices/tripSlice';
import { getCurrentUser } from '../redux/slices/authSlice';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { activeTrips } = useSelector((state) => state.trip);

  useEffect(() => {
    dispatch(getCurrentUser());
    dispatch(fetchMyTrips());
  }, [dispatch]);

  if (!user) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome, {user.first_name || user.username}!
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                User Type
              </Typography>
              <Typography variant="h4">
                {user?.user_type || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Active Trips
              </Typography>
              <Typography variant="h4">
                {activeTrips?.length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Rating
              </Typography>
              <Typography variant="h4">
                {user?.average_rating?.toFixed(1) || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          Active Trips
        </Typography>
        {activeTrips && activeTrips.length > 0 ? (
          activeTrips.map((trip) => (
            <Card key={trip.id} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6">
                  {trip.start_location_name} → {trip.end_location_name}
                </Typography>
                <Typography color="textSecondary">
                  Status: {trip.status}
                </Typography>
              </CardContent>
            </Card>
          ))
        ) : (
          <Typography>No active trips</Typography>
        )}
      </Paper>
    </Box>
  );
};

export default Dashboard;
