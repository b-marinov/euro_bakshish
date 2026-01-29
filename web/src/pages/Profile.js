import React from 'react';
import { useSelector } from 'react-redux';
import { Box, Typography, Paper, Avatar, Grid, Divider } from '@mui/material';

const Profile = () => {
  const { user } = useSelector((state) => state.auth);

  if (!user) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="center">
            <Avatar
              src={user.profile_picture}
              sx={{ width: 120, height: 120 }}
            >
              {user.first_name?.[0]}{user.last_name?.[0]}
            </Avatar>
          </Grid>
          
          <Grid item xs={12}>
            <Typography variant="h5" align="center">
              {user.first_name} {user.last_name}
            </Typography>
            <Typography variant="body1" align="center" color="textSecondary">
              @{user.username}
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Divider />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="textSecondary">
              Email
            </Typography>
            <Typography variant="body1">
              {user.email}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="textSecondary">
              Phone
            </Typography>
            <Typography variant="body1">
              {user.phone_number || 'Not provided'}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="textSecondary">
              User Type
            </Typography>
            <Typography variant="body1">
              {user.user_type}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="textSecondary">
              Average Rating
            </Typography>
            <Typography variant="body1">
              {user.average_rating ? user.average_rating.toFixed(2) : 'No ratings yet'}
            </Typography>
          </Grid>
          
          {user.passenger_profile && (
            <>
              <Grid item xs={12}>
                <Divider />
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Passenger Profile
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Total Trips
                </Typography>
                <Typography variant="body1">
                  {user.passenger_profile.total_trips}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Rating
                </Typography>
                <Typography variant="body1">
                  {user.passenger_profile.average_rating || 'No ratings'}
                </Typography>
              </Grid>
            </>
          )}
          
          {user.driver_profile && (
            <>
              <Grid item xs={12}>
                <Divider />
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Driver Profile
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Vehicle
                </Typography>
                <Typography variant="body1">
                  {user.driver_profile.vehicle_make} {user.driver_profile.vehicle_model} ({user.driver_profile.vehicle_year})
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Plate Number
                </Typography>
                <Typography variant="body1">
                  {user.driver_profile.vehicle_plate_number}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Total Trips
                </Typography>
                <Typography variant="body1">
                  {user.driver_profile.total_trips}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Rating
                </Typography>
                <Typography variant="body1">
                  {user.driver_profile.average_rating || 'No ratings'}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Status
                </Typography>
                <Typography variant="body1">
                  {user.driver_profile.is_verified ? 'Verified' : 'Not Verified'}
                </Typography>
              </Grid>
            </>
          )}
        </Grid>
      </Paper>
    </Box>
  );
};

export default Profile;
