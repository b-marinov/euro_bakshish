import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, Typography, TextField, Button, Alert
} from '@mui/material';
import { tripService } from '../services/services';

const TripPlanner = () => {
  const [formData, setFormData] = useState({
    start_location_name: '',
    start_latitude: '',
    start_longitude: '',
    end_location_name: '',
    end_latitude: '',
    end_longitude: '',
    passenger_notes: '',
    number_of_passengers: 1,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await tripService.createTrip(formData);
      setSuccess(true);
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err) {
      setError('Failed to create trip. Please try again.');
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Plan a Trip
      </Typography>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Trip created successfully! Redirecting...</Alert>}
        
        <form onSubmit={handleSubmit}>
          <Typography variant="h6" gutterBottom>
            Start Location
          </Typography>
          <TextField
            fullWidth
            name="start_location_name"
            label="Start Location Name"
            variant="outlined"
            margin="normal"
            value={formData.start_location_name}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="start_latitude"
            label="Start Latitude"
            type="number"
            variant="outlined"
            margin="normal"
            value={formData.start_latitude}
            onChange={handleChange}
            inputProps={{ step: 'any' }}
            required
          />
          <TextField
            fullWidth
            name="start_longitude"
            label="Start Longitude"
            type="number"
            variant="outlined"
            margin="normal"
            value={formData.start_longitude}
            onChange={handleChange}
            inputProps={{ step: 'any' }}
            required
          />
          
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            End Location
          </Typography>
          <TextField
            fullWidth
            name="end_location_name"
            label="End Location Name"
            variant="outlined"
            margin="normal"
            value={formData.end_location_name}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="end_latitude"
            label="End Latitude"
            type="number"
            variant="outlined"
            margin="normal"
            value={formData.end_latitude}
            onChange={handleChange}
            inputProps={{ step: 'any' }}
            required
          />
          <TextField
            fullWidth
            name="end_longitude"
            label="End Longitude"
            type="number"
            variant="outlined"
            margin="normal"
            value={formData.end_longitude}
            onChange={handleChange}
            inputProps={{ step: 'any' }}
            required
          />
          
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Additional Details
          </Typography>
          <TextField
            fullWidth
            name="number_of_passengers"
            label="Number of Passengers"
            type="number"
            variant="outlined"
            margin="normal"
            value={formData.number_of_passengers}
            onChange={handleChange}
            inputProps={{ min: 1, max: 8 }}
            required
          />
          <TextField
            fullWidth
            name="passenger_notes"
            label="Notes (Optional)"
            variant="outlined"
            margin="normal"
            multiline
            rows={3}
            value={formData.passenger_notes}
            onChange={handleChange}
          />
          
          <Button
            fullWidth
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >
            Create Trip
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default TripPlanner;
