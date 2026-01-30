"""
Simple test to verify the NextPy application can be imported and works
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that the application can be imported"""
    try:
        import euro_bakshish_app
        print("✓ Application imports successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_models():
    """Test that models are defined correctly"""
    try:
        from euro_bakshish_app import User, Trip, Review
        print("✓ Models imported successfully")
        
        # Check model fields
        assert hasattr(User, 'username')
        assert hasattr(User, 'email')
        assert hasattr(Trip, 'start_location_name')
        assert hasattr(Review, 'rating')
        print("✓ Model fields are correct")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    try:
        from euro_bakshish_app import init_db, engine
        from sqlmodel import Session, select
        from euro_bakshish_app import User
        
        # Initialize database
        init_db()
        print("✓ Database initialized")
        
        # Try to create a test user
        with Session(engine) as session:
            test_user = User(
                username="test_user",
                email="test@example.com",
                password_hash="test123",
                user_type="passenger"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            print(f"✓ Test user created with ID: {test_user.id}")
            
            # Query the user back
            statement = select(User).where(User.username == "test_user")
            user = session.exec(statement).first()
            assert user is not None
            assert user.username == "test_user"
            print("✓ User query successful")
            
            # Clean up
            session.delete(user)
            session.commit()
            print("✓ Cleanup successful")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing NextPy Euro Bakshish Application")
    print("=" * 50)
    
    results = []
    
    print("\n1. Testing Imports...")
    results.append(test_imports())
    
    print("\n2. Testing Models...")
    results.append(test_models())
    
    print("\n3. Testing Database...")
    results.append(test_database())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 50)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    exit(main())
