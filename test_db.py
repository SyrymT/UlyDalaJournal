from main import app, db
from models import User
import sys

print("Starting database test...")

try:
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        try:
            db.engine.connect()
            print("Database connection successful!")
            
            # Test creating a user
            test_user = User(username='testuser', email='test@example.com', password='password', full_name='Test User')
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully!")
            
            # Verify the user was created
            user = User.query.filter_by(username='testuser').first()
            if user:
                print(f"User found: {user.username}, {user.email}")
            else:
                print("User not found in the database.")
            
            # Clean up: remove the test user
            db.session.delete(user)
            db.session.commit()
            print("Test user removed from the database.")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print(f"Python version: {sys.version}")
    print(f"SQLAlchemy version: {db.engine.dialect.server_version_info}")

print("Database test completed.")