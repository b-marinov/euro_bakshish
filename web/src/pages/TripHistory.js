import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box, Typography, Paper, Card, CardContent,
  Tabs, Tab, Chip
} from '@mui/material';
import { fetchTripHistory } from '../redux/slices/tripSlice';

const TripHistory = () => {
  const [tabValue, setTabValue] = React.useState(0);
  const dispatch = useDispatch();
  const { tripHistory } = useSelector((state) => state.trip);

  useEffect(() => {
    const role = tabValue === 0 ? 'all' : tabValue === 1 ? 'passenger' : 'driver';
    dispatch(fetchTripHistory(role));
  }, [dispatch, tabValue]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Trip History
      </Typography>
      
      <Paper sx={{ mt: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} centered>
          <Tab label="All Trips" />
          <Tab label="As Passenger" />
          <Tab label="As Driver" />
        </Tabs>
        
        <Box sx={{ p: 3 }}>
          {tripHistory && tripHistory.length > 0 ? (
            tripHistory.map((trip) => (
              <Card key={trip.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="h6">
                      {trip.start_location_name} → {trip.end_location_name}
                    </Typography>
                    <Chip
                      label={trip.status}
                      color={getStatusColor(trip.status)}
                      size="small"
                    />
                  </Box>
                  
                  <Typography color="textSecondary" sx={{ mt: 1 }}>
                    Passenger: {trip.passenger_name}
                  </Typography>
                  {trip.driver_name && (
                    <Typography color="textSecondary">
                      Driver: {trip.driver_name}
                    </Typography>
                  )}
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2">
                      Distance: {trip.distance_km ? `${trip.distance_km} km` : 'N/A'}
                    </Typography>
                    <Typography variant="body2">
                      Fare: {trip.fare ? `€${trip.fare}` : 'N/A'}
                    </Typography>
                    <Typography variant="body2">
                      Completed: {trip.completed_at ? new Date(trip.completed_at).toLocaleString() : 'N/A'}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mt: 2 }}>
                    {trip.has_passenger_review ? (
                      <Chip label="Passenger Reviewed" color="success" size="small" sx={{ mr: 1 }} />
                    ) : (
                      <Chip label="Passenger Review Pending" color="warning" size="small" sx={{ mr: 1 }} />
                    )}
                    {trip.has_driver_review ? (
                      <Chip label="Driver Reviewed" color="success" size="small" />
                    ) : (
                      <Chip label="Driver Review Pending" color="warning" size="small" />
                    )}
                  </Box>
                </CardContent>
              </Card>
            ))
          ) : (
            <Typography align="center">No trip history</Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default TripHistory;
