# Quick Start Guide - Euro Bakshish (NextPy)

Get started with the Euro Bakshish ride-sharing application in minutes!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

That's it! No Node.js, no Android Studio, no additional setup required.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish
```

### 2. Install Dependencies

```bash
pip install -r requirements-nextpy.txt
```

### 3. Run the Application

```bash
python euro_bakshish_app.py
```

The application will:
- Create the database automatically
- Start both backend and frontend servers
- Open your browser to http://localhost:3000

## First Steps

### 1. Register a New User
1. Go to http://localhost:3000
2. Click "Register here"
3. Fill in your details and user type
4. Click "Register"

### 2. Login
1. Enter your credentials
2. Click "Login"

### 3. Create a Trip
1. Click "Create New Trip"
2. Fill in trip details
3. Click "Create Trip"

## Common Tasks

### View Database
```bash
sqlite3 euro_bakshish.db
.tables
SELECT * FROM user;
```

### Reset Database
```bash
rm euro_bakshish.db
python euro_bakshish_app.py
```

## Troubleshooting

See [README.md](README.md) for detailed information.

Happy coding! 🚀
