# Project Overview - Euro Bakshish

## 📁 Project Structure

```
euro_bakshish/
├── 📱 euro_bakshish_app.py     # Main NextPy Application  
│   ├── Database Models         # User, Trip, Review models
│   ├── Application State       # State management
│   ├── API Endpoints          # Automatically generated
│   └── UI Components          # Login, Register, Dashboard, etc.
│
├── 📦 requirements-nextpy.txt  # Python dependencies
│
├── 🗄️ euro_bakshish.db         # SQLite database (auto-created)
│
└── 📚 docs/                    # Project documentation
    ├── ARCHITECTURE.md         # System architecture
    ├── SETUP.md                # Setup guide
    └── SECURITY.md             # Security best practices
```

## 🎯 Architecture

### Current Architecture (NextPy-based)
- **Full Stack**: NextPy (Pure Python)
- **Frontend**: React components via Python (no JavaScript!)
- **Backend**: FastAPI (built into NextPy)
- **Database**: SQLModel (SQLite/PostgreSQL)
- **Authentication**: Built-in session management
- **Complexity**: Single codebase, single language, simple deployment

## 🔧 Technology Stack

### NextPy Stack
- **NextPy**: Pure Python full-stack framework
- **SQLModel**: SQL database ORM (built on SQLAlchemy + Pydantic)
- **FastAPI**: High-performance API (built into NextPy)
- **React**: UI rendering (via NextPy, no JS needed)
- **SQLite/PostgreSQL**: Database options

### Benefits of NextPy
- **Single Language**: Everything in Python - no context switching
- **Unified Codebase**: Frontend and backend in one file
- **Type Safety**: Pydantic models ensure data validation
- **Auto-Generated API**: REST API created automatically
- **Hot Reload**: Fast development with instant updates
- **Easy Deployment**: Single Python app to deploy
- **AI-Ready**: Built-in support for AI/LLM integration

## 🎯 Core Features

All features implemented:

### 1. User Management
- **Registration**: Create accounts as Passenger, Driver, or Both
- **Authentication**: Secure session-based authentication
- **Profiles**: User profile management with all necessary fields

### 2. Trip Management
- **Trip Creation**: Passengers request trips with start/end locations
- **Trip States**: pending → accepted → in_progress → completed
- **Driver Operations**: Accept, start, and complete trips
- **Trip History**: Complete history for both passengers and drivers

### 3. Rating System
- **Mutual Reviews**: Both passengers and drivers rate each other
- **Multi-dimensional Ratings**: Overall + category-specific ratings
- **Automatic Calculations**: User ratings update automatically

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements-nextpy.txt

# Run the application
python euro_bakshish_app.py

# Access at http://localhost:3000
```

## 👥 Project Status

✅ **Active** - NextPy full-stack application

---

**Euro Bakshish** - A modern ride-sharing platform 🚗✨
