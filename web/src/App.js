import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from '@mui/material';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import TripPlanner from './pages/TripPlanner';
import TripHistory from './pages/TripHistory';
import NavBar from './components/NavBar';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <div className="App">
      <NavBar />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route
            path="/plan-trip"
            element={
              <PrivateRoute>
                <TripPlanner />
              </PrivateRoute>
            }
          />
          <Route
            path="/trip-history"
            element={
              <PrivateRoute>
                <TripHistory />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;
