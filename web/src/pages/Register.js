import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, TextField, Button, Typography, Alert,
  FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import { authService } from '../services/services';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    user_type: 'passenger',
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
    
    if (formData.password !== formData.password2) {
      setError('Passwords do not match');
      return;
    }

    try {
      await authService.register(formData);
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
      <Paper elevation={3} sx={{ p: 4, maxWidth: 500, width: '100%' }}>
        <Typography variant="h5" component="h1" gutterBottom align="center">
          Register
        </Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Registration successful! Redirecting to login...</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            name="username"
            label="Username"
            variant="outlined"
            margin="normal"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="email"
            label="Email"
            type="email"
            variant="outlined"
            margin="normal"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="first_name"
            label="First Name"
            variant="outlined"
            margin="normal"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="last_name"
            label="Last Name"
            variant="outlined"
            margin="normal"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="phone_number"
            label="Phone Number"
            variant="outlined"
            margin="normal"
            value={formData.phone_number}
            onChange={handleChange}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>User Type</InputLabel>
            <Select
              name="user_type"
              value={formData.user_type}
              onChange={handleChange}
              label="User Type"
            >
              <MenuItem value="passenger">Passenger</MenuItem>
              <MenuItem value="driver">Driver</MenuItem>
              <MenuItem value="both">Both</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            name="password"
            label="Password"
            type="password"
            variant="outlined"
            margin="normal"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            name="password2"
            label="Confirm Password"
            type="password"
            variant="outlined"
            margin="normal"
            value={formData.password2}
            onChange={handleChange}
            required
          />
          <Button
            fullWidth
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >
            Register
          </Button>
          <Button
            fullWidth
            variant="text"
            sx={{ mt: 1 }}
            onClick={() => navigate('/login')}
          >
            Already have an account? Login
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default Register;
