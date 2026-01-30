"""
Pytest configuration and fixtures for Euro Bakshish tests.
"""
import os
import pytest
from sqlmodel import Session, SQLModel, create_engine
from euro_bakshish_app import User, Trip, Review, hash_password


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine."""
    # Use in-memory SQLite for tests
    database_url = "sqlite:///:memory:"
    engine = create_engine(database_url, echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_db_engine):
    """Create a new database session for a test."""
    with Session(test_db_engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("password123"),
        user_type="passenger"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_driver(db_session):
    """Create a sample driver for testing."""
    driver = User(
        username="testdriver",
        email="driver@example.com",
        password_hash=hash_password("password123"),
        user_type="driver",
        license_number="DL123456",
        vehicle_make="Toyota",
        vehicle_model="Camry",
        vehicle_year=2020,
        vehicle_color="Blue",
        vehicle_plate_number="ABC123",
        is_verified=True
    )
    db_session.add(driver)
    db_session.commit()
    db_session.refresh(driver)
    return driver


@pytest.fixture
def sample_trip(db_session, sample_user):
    """Create a sample trip for testing."""
    trip = Trip(
        passenger_id=sample_user.id,
        start_location_name="Downtown",
        start_latitude=40.7128,
        start_longitude=-74.0060,
        end_location_name="Airport",
        end_latitude=40.6413,
        end_longitude=-73.7781,
        status="pending",
        number_of_passengers=2
    )
    db_session.add(trip)
    db_session.commit()
    db_session.refresh(trip)
    return trip
