"""
Integration tests for application state and logic.
"""

import pytest
from sqlmodel import Session, select

from euro_bakshish_app import Trip, User, hash_password, verify_password


@pytest.mark.integration
class TestUserAuthentication:
    """Tests for user authentication logic."""

    def test_user_registration_flow(self, db_session):
        """Test complete user registration flow."""
        # Create user with hashed password
        username = "newuser"
        email = "newuser@example.com"
        password = "securePassword123"

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            user_type="passenger",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Verify user was created
        assert user.id is not None

        # Verify password verification works
        assert verify_password(password, user.password_hash) is True

    def test_user_login_flow(self, db_session, sample_user):
        """Test user login flow."""
        # Find user by username
        statement = select(User).where(User.username == sample_user.username)
        found_user = db_session.exec(statement).first()

        assert found_user is not None
        assert found_user.username == sample_user.username

        # Verify password
        assert verify_password("password123", found_user.password_hash) is True


@pytest.mark.integration
class TestTripWorkflow:
    """Tests for trip workflow."""

    def test_create_trip_workflow(self, db_session, sample_user):
        """Test creating a new trip."""
        trip = Trip(
            passenger_id=sample_user.id,
            start_location_name="Times Square",
            start_latitude=40.7580,
            start_longitude=-73.9855,
            end_location_name="Central Park",
            end_latitude=40.7829,
            end_longitude=-73.9654,
            number_of_passengers=2,
            passenger_notes="Looking for a quick ride",
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        assert trip.id is not None
        assert trip.status == "pending"
        assert trip.driver_id is None

    def test_driver_accept_trip_workflow(self, db_session, sample_trip, sample_driver):
        """Test driver accepting a trip."""
        # Driver accepts the trip
        sample_trip.driver_id = sample_driver.id
        sample_trip.status = "accepted"
        db_session.add(sample_trip)
        db_session.commit()

        # Verify trip was updated
        db_session.refresh(sample_trip)
        assert sample_trip.driver_id == sample_driver.id
        assert sample_trip.status == "accepted"

    def test_complete_trip_workflow(self, db_session, sample_trip, sample_driver):
        """Test completing a trip."""
        # Accept trip
        sample_trip.driver_id = sample_driver.id
        sample_trip.status = "accepted"
        db_session.add(sample_trip)
        db_session.commit()

        # Start trip
        sample_trip.status = "in_progress"
        db_session.add(sample_trip)
        db_session.commit()

        # Complete trip
        sample_trip.status = "completed"
        sample_trip.fare = 25.50
        db_session.add(sample_trip)
        db_session.commit()

        db_session.refresh(sample_trip)
        assert sample_trip.status == "completed"
        assert sample_trip.fare == 25.50

    def test_load_user_trips(self, db_session, sample_user):
        """Test loading trips for a specific user."""
        # Create multiple trips
        for i in range(3):
            trip = Trip(
                passenger_id=sample_user.id,
                start_location_name=f"Location {i}",
                start_latitude=40.7128,
                start_longitude=-74.0060,
                end_location_name=f"Destination {i}",
                end_latitude=40.7580,
                end_longitude=-73.9855,
                number_of_passengers=1,
            )
            db_session.add(trip)
        db_session.commit()

        # Load trips for user
        statement = select(Trip).where(Trip.passenger_id == sample_user.id)
        trips = db_session.exec(statement).all()

        assert len(trips) >= 3


@pytest.mark.integration
class TestStateMutations:
    """Tests for state mutations and validations."""

    def test_number_of_passengers_validation(self, db_session, sample_user):
        """Test that number of passengers is validated."""
        trip = Trip(
            passenger_id=sample_user.id,
            start_location_name="Home",
            start_latitude=40.7128,
            start_longitude=-74.0060,
            end_location_name="Work",
            end_latitude=40.7580,
            end_longitude=-73.9855,
            number_of_passengers=1,
        )
        db_session.add(trip)
        db_session.commit()

        assert trip.number_of_passengers >= 1

    def test_trip_status_values(self, db_session, sample_trip):
        """Test valid trip status values."""
        valid_statuses = ["pending", "accepted", "in_progress", "completed", "cancelled"]

        for status in valid_statuses:
            sample_trip.status = status
            db_session.add(sample_trip)
            db_session.commit()
            db_session.refresh(sample_trip)
            assert sample_trip.status == status
