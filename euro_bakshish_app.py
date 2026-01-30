"""
Euro Bakshish - Ride Sharing Application
Built with NextPy Framework

This application replaces the previous Django + React + Android stack
with a unified NextPy application for both backend and frontend.
"""

import nextpy as xt
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

# Database Models

class User(SQLModel, table=True):
    """User model for both passengers and drivers"""
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    user_type: str = Field(default="passenger")  # passenger, driver, or both
    phone_number: str = Field(default="")
    date_of_birth: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Profile fields
    preferred_payment_method: str = Field(default="cash")
    emergency_contact_name: str = Field(default="")
    emergency_contact_phone: str = Field(default="")
    
    # Driver specific fields
    license_number: str = Field(default="")
    license_expiry: Optional[datetime] = None
    vehicle_make: str = Field(default="")
    vehicle_model: str = Field(default="")
    vehicle_year: Optional[int] = None
    vehicle_color: str = Field(default="")
    vehicle_plate_number: str = Field(default="")
    vehicle_capacity: int = Field(default=4)
    insurance_number: str = Field(default="")
    insurance_expiry: Optional[datetime] = None
    is_verified: bool = Field(default=False)
    is_available: bool = Field(default=False)
    
    # Statistics
    total_trips_as_passenger: int = Field(default=0)
    total_trips_as_driver: int = Field(default=0)
    average_rating_as_passenger: Optional[float] = None
    average_rating_as_driver: Optional[float] = None


class Trip(SQLModel, table=True):
    """Trip model for ride sharing"""
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    passenger_id: int = Field(foreign_key="user.id")
    driver_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Location details
    start_location_name: str
    start_latitude: float
    start_longitude: float
    end_location_name: str
    end_latitude: float
    end_longitude: float
    
    # Trip details
    status: str = Field(default="pending")  # pending, accepted, in_progress, completed, cancelled
    distance_km: Optional[float] = None
    estimated_duration_minutes: Optional[int] = None
    fare: Optional[float] = None
    
    # Timestamps
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    # Additional info
    passenger_notes: str = Field(default="")
    driver_notes: str = Field(default="")
    number_of_passengers: int = Field(default=1)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Review(SQLModel, table=True):
    """Review/Rating model"""
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(foreign_key="trip.id")
    reviewer_id: int = Field(foreign_key="user.id")
    reviewed_user_id: int = Field(foreign_key="user.id")
    
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="")
    
    # Category ratings
    punctuality_rating: Optional[int] = Field(default=None, ge=1, le=5)
    cleanliness_rating: Optional[int] = Field(default=None, ge=1, le=5)
    safety_rating: Optional[int] = Field(default=None, ge=1, le=5)
    communication_rating: Optional[int] = Field(default=None, ge=1, le=5)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Database setup
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./euro_bakshish.db")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize database tables"""
    # Ensure the directory exists if using SQLite database
    if DATABASE_URL.startswith("sqlite:"):
        # Extract the file path from SQLite URL (handles sqlite:/// format)
        db_path = DATABASE_URL.split("sqlite:///")[-1] if "sqlite:///" in DATABASE_URL else DATABASE_URL.split("sqlite://")[-1]
        # Normalize the path and get directory
        db_path = os.path.normpath(db_path)
        db_dir = os.path.dirname(db_path)
        # Create directory if it's not empty and not current directory
        if db_dir and db_dir != ".":
            os.makedirs(db_dir, exist_ok=True)
    SQLModel.metadata.create_all(engine)


# Application State
class State(xt.State):
    """Main application state"""
    # Authentication
    logged_in: bool = False
    current_user: Optional[dict] = None
    
    # Forms
    username: str = ""
    email: str = ""
    password: str = ""
    user_type: str = "passenger"
    
    # Trip creation
    start_location: str = ""
    end_location: str = ""
    start_lat: float = 0.0
    start_lon: float = 0.0
    end_lat: float = 0.0
    end_lon: float = 0.0
    num_passengers: str = "1"
    passenger_notes: str = ""
    
    # Data lists
    trips: List[dict] = []
    available_trips: List[dict] = []
    reviews: List[dict] = []
    
    # UI state
    show_trip_form: bool = False
    selected_trip_id: Optional[int] = None
    error_message: str = ""
    success_message: str = ""
    
    def login(self):
        """Handle user login"""
        with Session(engine) as session:
            statement = select(User).where(User.username == self.username)
            user = session.exec(statement).first()
            
            if user and verify_password(self.password, user.password_hash):
                self.logged_in = True
                self.current_user = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "user_type": user.user_type
                }
                self.success_message = "Login successful!"
                self.error_message = ""
            else:
                self.error_message = "Invalid username or password"
                self.success_message = ""
    
    def register(self):
        """Handle user registration"""
        with Session(engine) as session:
            # Check if user already exists
            statement = select(User).where(User.username == self.username)
            existing_user = session.exec(statement).first()
            
            if existing_user:
                self.error_message = "Username already exists"
                self.success_message = ""
                return
            
            # Create new user with hashed password
            new_user = User(
                username=self.username,
                email=self.email,
                password_hash=hash_password(self.password),  # Secure password hashing
                user_type=self.user_type
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            
            self.success_message = "Registration successful! Please login."
            self.error_message = ""
            self.username = ""
            self.email = ""
            self.password = ""
    
    def logout(self):
        """Handle user logout"""
        self.logged_in = False
        self.current_user = None
        self.success_message = "Logged out successfully"
    
    def create_trip(self):
        """Create a new trip"""
        if not self.logged_in or not self.current_user:
            self.error_message = "Please login first"
            return
        
        # Validate num_passengers input
        try:
            num_pass = int(self.num_passengers) if self.num_passengers else 1
            if num_pass < 1:
                self.error_message = "Number of passengers must be at least 1"
                return
        except (ValueError, TypeError):
            self.error_message = "Please enter a valid number of passengers"
            return
        
        with Session(engine) as session:
            new_trip = Trip(
                passenger_id=self.current_user["id"],
                start_location_name=self.start_location,
                start_latitude=self.start_lat,
                start_longitude=self.start_lon,
                end_location_name=self.end_location,
                end_latitude=self.end_lat,
                end_longitude=self.end_lon,
                number_of_passengers=num_pass,
                passenger_notes=self.passenger_notes
            )
            session.add(new_trip)
            session.commit()
            
            self.success_message = "Trip created successfully!"
            self.error_message = ""
            self.show_trip_form = False
            self.load_trips()
    
    def load_trips(self):
        """Load trips for current user"""
        if not self.logged_in or not self.current_user:
            return
        
        with Session(engine) as session:
            statement = select(Trip).where(Trip.passenger_id == self.current_user["id"])
            trips = session.exec(statement).all()
            
            self.trips = [
                {
                    "id": trip.id,
                    "start": trip.start_location_name,
                    "end": trip.end_location_name,
                    "status": trip.status,
                    "created_at": trip.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for trip in trips
            ]
    
    def accept_trip(self, trip_id: int):
        """Driver accepts a trip"""
        if not self.logged_in or not self.current_user:
            return
        
        with Session(engine) as session:
            trip = session.get(Trip, trip_id)
            if trip and trip.status == "pending":
                trip.driver_id = self.current_user["id"]
                trip.status = "accepted"
                trip.accepted_at = datetime.now(timezone.utc)
                session.add(trip)
                session.commit()
                
                self.success_message = "Trip accepted!"
                self.load_available_trips()
    
    def load_available_trips(self):
        """Load available trips for drivers"""
        if not self.logged_in or not self.current_user:
            return
        
        with Session(engine) as session:
            statement = select(Trip).where(Trip.status == "pending")
            trips = session.exec(statement).all()
            
            self.available_trips = [
                {
                    "id": trip.id,
                    "start": trip.start_location_name,
                    "end": trip.end_location_name,
                    "passengers": trip.number_of_passengers,
                    "created_at": trip.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for trip in trips
            ]


# UI Components

def navbar() -> xt.Component:
    """Navigation bar component"""
    return xt.box(
        xt.hstack(
            xt.heading("Euro Bakshish", size="lg"),
            xt.spacer(),
            xt.cond(
                State.logged_in,
                xt.hstack(
                    xt.text("Welcome, " + State.username),
                    xt.button("Logout", on_click=State.logout),
                ),
                xt.hstack(
                    xt.link("Login", href="/"),
                    xt.link("Register", href="/register"),
                )
            ),
            spacing="4",
        ),
        bg="blue.500",
        color="white",
        padding="4",
    )


def login_page() -> xt.Component:
    """Login page"""
    return xt.box(
        navbar(),
        xt.center(
            xt.vstack(
                xt.heading("Login", size="xl"),
                xt.input(placeholder="Username", value=State.username, on_change=State.set_username),
                xt.input(placeholder="Password", type_="password", value=State.password, on_change=State.set_password),
                xt.button("Login", on_click=State.login),
                xt.cond(
                    State.error_message != "",
                    xt.text(State.error_message, color="red"),
                ),
                xt.cond(
                    State.success_message != "",
                    xt.text(State.success_message, color="green"),
                ),
                xt.link("Don't have an account? Register here", href="/register"),
                spacing="4",
                width="400px",
                padding="8",
            ),
            height="100vh",
        ),
    )


def register_page() -> xt.Component:
    """Registration page"""
    return xt.box(
        navbar(),
        xt.center(
            xt.vstack(
                xt.heading("Register", size="xl"),
                xt.input(placeholder="Username", value=State.username, on_change=State.set_username),
                xt.input(placeholder="Email", value=State.email, on_change=State.set_email),
                xt.input(placeholder="Password", type_="password", value=State.password, on_change=State.set_password),
                xt.select(
                    ["passenger", "driver", "both"],
                    placeholder="User Type",
                    value=State.user_type,
                    on_change=State.set_user_type,
                ),
                xt.button("Register", on_click=State.register),
                xt.cond(
                    State.error_message != "",
                    xt.text(State.error_message, color="red"),
                ),
                xt.cond(
                    State.success_message != "",
                    xt.text(State.success_message, color="green"),
                ),
                xt.link("Already have an account? Login here", href="/"),
                spacing="4",
                width="400px",
                padding="8",
            ),
            height="100vh",
        ),
    )


def dashboard() -> xt.Component:
    """Main dashboard"""
    return xt.cond(
        State.logged_in,
        xt.box(
            navbar(),
            xt.container(
                xt.vstack(
                    xt.heading("Dashboard", size="xl"),
                    xt.cond(
                        State.success_message != "",
                        xt.text(State.success_message, color="green"),
                    ),
                    xt.button("Create New Trip", on_click=lambda: State.set_show_trip_form(True)),
                    xt.cond(
                        State.show_trip_form,
                        xt.vstack(
                            xt.heading("New Trip", size="lg"),
                            xt.input(placeholder="Start Location", value=State.start_location, on_change=State.set_start_location),
                            xt.input(placeholder="End Location", value=State.end_location, on_change=State.set_end_location),
                            xt.input(placeholder="Number of Passengers", type_="number", value=State.num_passengers, on_change=State.set_num_passengers),
                            xt.text_area(placeholder="Notes", value=State.passenger_notes, on_change=State.set_passenger_notes),
                            xt.button("Create Trip", on_click=State.create_trip),
                            spacing="3",
                            border="1px solid gray",
                            padding="4",
                            border_radius="md",
                        ),
                    ),
                    xt.heading("My Trips", size="lg"),
                    xt.foreach(
                        State.trips,
                        lambda trip: xt.box(
                            xt.text(f"From: {trip['start']} To: {trip['end']}"),
                            xt.text(f"Status: {trip['status']}"),
                            xt.text(f"Created: {trip['created_at']}"),
                            border="1px solid gray",
                            padding="3",
                            margin="2",
                            border_radius="md",
                        ),
                    ),
                    spacing="4",
                    padding="8",
                ),
                max_width="800px",
            ),
        ),
        xt.center(
            xt.text("Please login to access dashboard"),
        ),
    )


# App configuration
app = xt.App()

# Add pages
app.add_page(login_page, route="/")
app.add_page(register_page, route="/register")
app.add_page(dashboard, route="/dashboard", on_load=State.load_trips)

# Initialize database
init_db()

