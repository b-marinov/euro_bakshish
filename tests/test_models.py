"""
Unit tests for database models.
"""
import pytest
from datetime import datetime, timezone
from euro_bakshish_app import User, Trip, Review, hash_password, verify_password


@pytest.mark.unit
class TestUserModel:
    """Tests for User model."""

    def test_create_passenger_user(self, db_session):
        """Test creating a passenger user."""
        user = User(
            username="passenger1",
            email="passenger1@example.com",
            password_hash=hash_password("securepass"),
            user_type="passenger"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.username == "passenger1"
        assert user.email == "passenger1@example.com"
        assert user.user_type == "passenger"
        assert user.created_at is not None

    def test_create_driver_user(self, db_session):
        """Test creating a driver user."""
        user = User(
            username="driver1",
            email="driver1@example.com",
            password_hash=hash_password("securepass"),
            user_type="driver",
            license_number="DL987654",
            vehicle_make="Honda",
            vehicle_model="Accord",
            vehicle_year=2021
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.user_type == "driver"
        assert user.license_number == "DL987654"
        assert user.vehicle_make == "Honda"

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "mySecurePassword123"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongPassword", hashed) is False

    def test_user_unique_constraints(self, db_session, sample_user):
        """Test that username and email must be unique."""
        # Try to create user with same username
        duplicate_user = User(
            username=sample_user.username,
            email="different@example.com",
            password_hash=hash_password("password"),
            user_type="passenger"
        )
        db_session.add(duplicate_user)

        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


@pytest.mark.unit
class TestTripModel:
    """Tests for Trip model."""

    def test_create_trip(self, db_session, sample_user):
        """Test creating a trip."""
        trip = Trip(
            passenger_id=sample_user.id,
            start_location_name="Home",
            start_latitude=40.7128,
            start_longitude=-74.0060,
            end_location_name="Work",
            end_latitude=40.7580,
            end_longitude=-73.9855,
            status="pending",
            number_of_passengers=1
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        assert trip.id is not None
        assert trip.passenger_id == sample_user.id
        assert trip.status == "pending"
        assert trip.start_location_name == "Home"
        assert trip.driver_id is None

    def test_trip_status_transitions(self, db_session, sample_trip, sample_driver):
        """Test trip status transitions."""
        # Initially pending
        assert sample_trip.status == "pending"

        # Accept trip
        sample_trip.driver_id = sample_driver.id
        sample_trip.status = "accepted"
        sample_trip.accepted_at = datetime.now(timezone.utc)
        db_session.add(sample_trip)
        db_session.commit()

        assert sample_trip.status == "accepted"
        assert sample_trip.driver_id == sample_driver.id
        assert sample_trip.accepted_at is not None

    def test_trip_with_notes(self, db_session, sample_user):
        """Test trip with passenger notes."""
        trip = Trip(
            passenger_id=sample_user.id,
            start_location_name="Home",
            start_latitude=40.7128,
            start_longitude=-74.0060,
            end_location_name="Airport",
            end_latitude=40.6413,
            end_longitude=-73.7781,
            passenger_notes="Please wait at main entrance",
            number_of_passengers=3
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        assert trip.passenger_notes == "Please wait at main entrance"
        assert trip.number_of_passengers == 3


@pytest.mark.unit
class TestReviewModel:
    """Tests for Review model."""

    def test_create_review(self, db_session, sample_trip, sample_user, sample_driver):
        """Test creating a review."""
        # First complete the trip
        sample_trip.driver_id = sample_driver.id
        sample_trip.status = "completed"
        db_session.add(sample_trip)
        db_session.commit()

        # Create review
        review = Review(
            trip_id=sample_trip.id,
            reviewer_id=sample_user.id,
            reviewed_user_id=sample_driver.id,
            rating=5,
            comment="Excellent driver!",
            punctuality_rating=5,
            cleanliness_rating=5,
            safety_rating=5
        )
        db_session.add(review)
        db_session.commit()
        db_session.refresh(review)

        assert review.id is not None
        assert review.rating == 5
        assert review.comment == "Excellent driver!"

    def test_review_rating_constraints(self, db_session, sample_trip, sample_user, sample_driver):
        """Test that ratings are constrained between 1 and 5."""
        sample_trip.driver_id = sample_driver.id
        db_session.add(sample_trip)
        db_session.commit()

        # Valid rating
        review = Review(
            trip_id=sample_trip.id,
            reviewer_id=sample_user.id,
            reviewed_user_id=sample_driver.id,
            rating=3
        )
        db_session.add(review)
        db_session.commit()
        assert review.rating == 3
