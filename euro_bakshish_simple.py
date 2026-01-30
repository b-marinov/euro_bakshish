"""
Euro Bakshish - Simplified NextPy Application
This is a simplified demonstration version showing the NextPy architecture.
"""

import nextpy as xt
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Database Models

class User(SQLModel, table=True):
    """User model"""
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str
    password: str  # In production, use proper hashing
    user_type: str = Field(default="passenger")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Trip(SQLModel, table=True):
    """Trip model"""
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    passenger_id: int
    start_location: str
    end_location: str
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Database setup
DATABASE_URL = "sqlite:///./euro_bakshish.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

# Application State
class AppState(xt.State):
    """Application state"""
    logged_in: bool = False
    username: str = ""
    email: str = ""
    password: str = ""
    message: str = ""
    
    def register(self):
        """Register new user"""
        if not self.username or not self.password:
            self.message = "Please fill all fields"
            return
            
        with Session(engine) as session:
            user = User(
                username=self.username,
                email=self.email,
                password=self.password
            )
            session.add(user)
            try:
                session.commit()
                self.message = "Registration successful!"
                self.username = ""
                self.email = ""
                self.password = ""
            except Exception as e:
                self.message = f"Error: {str(e)}"
    
    def login(self):
        """Login user"""
        with Session(engine) as session:
            statement = select(User).where(User.username == self.username)
            user = session.exec(statement).first()
            
            if user and user.password == self.password:
                self.logged_in = True
                self.message = "Login successful!"
            else:
                self.message = "Invalid credentials"
    
    def logout(self):
        """Logout user"""
        self.logged_in = False
        self.username = ""
        self.password = ""
        self.message = "Logged out"

# UI Components

def index() -> xt.Component:
    """Main page"""
    return xt.center(
        xt.vstack(
            xt.heading("Euro Bakshish", size="2xl"),
            xt.text("Ride Sharing Application", size="lg"),
            xt.cond(
                AppState.logged_in,
                xt.vstack(
                    xt.text("Welcome! You are logged in.", color="green"),
                    xt.button("Logout", on_click=AppState.logout),
                ),
                xt.vstack(
                    xt.heading("Login", size="lg"),
                    xt.input(
                        placeholder="Username",
                        value=AppState.username,
                        on_change=AppState.set_username,
                    ),
                    xt.input(
                        placeholder="Password",
                        type_="password",
                        value=AppState.password,
                        on_change=AppState.set_password,
                    ),
                    xt.button("Login", on_click=AppState.login),
                    xt.link("Register", href="/register"),
                ),
            ),
            xt.cond(
                AppState.message != "",
                xt.text(AppState.message),
            ),
            spacing="4",
            padding="8",
        ),
        height="100vh",
    )

def register() -> xt.Component:
    """Registration page"""
    return xt.center(
        xt.vstack(
            xt.heading("Register", size="xl"),
            xt.input(
                placeholder="Username",
                value=AppState.username,
                on_change=AppState.set_username,
            ),
            xt.input(
                placeholder="Email",
                value=AppState.email,
                on_change=AppState.set_email,
            ),
            xt.input(
                placeholder="Password",
                type_="password",
                value=AppState.password,
                on_change=AppState.set_password,
            ),
            xt.button("Register", on_click=AppState.register),
            xt.cond(
                AppState.message != "",
                xt.text(AppState.message),
            ),
            xt.link("Back to Login", href="/"),
            spacing="4",
            padding="8",
        ),
        height="100vh",
    )

# App setup
app = xt.App()
app.add_page(index)
app.add_page(register)

# Initialize database
init_db()

# Compile
app.compile_()
