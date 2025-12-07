"""
Test script for Flask Quiz Application
Tests basic functionality without requiring the server to be running
"""

import sys
from app import create_app, db
from app.models import User, Category, Question, Attempt, LeaderboardEntry, Competition

def test_app_creation():
    """Test if the app can be created"""
    print("Testing app creation...")
    try:
        app = create_app()
        print("✓ App created successfully")
        return app
    except Exception as e:
        print(f"✗ Failed to create app: {e}")
        return None

def test_database_connection(app):
    """Test database connection and models"""
    print("\nTesting database connection...")
    try:
        with app.app_context():
            # Test User model
            user_count = User.query.count()
            print(f"✓ Users in database: {user_count}")
            
            # Test Category model
            category_count = Category.query.count()
            print(f"✓ Categories in database: {category_count}")
            
            # Test Question model
            question_count = Question.query.count()
            print(f"✓ Questions in database: {question_count}")
            
            # Test Attempt model
            attempt_count = Attempt.query.count()
            print(f"✓ Attempts in database: {attempt_count}")
            
            # Test LeaderboardEntry model
            leaderboard_count = LeaderboardEntry.query.count()
            print(f"✓ Leaderboard entries: {leaderboard_count}")
            
            # Test Competition model
            competition_count = Competition.query.count()
            print(f"✓ Competitions in database: {competition_count}")
            
            return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_blueprints(app):
    """Test if all blueprints are registered"""
    print("\nTesting blueprints...")
    try:
        blueprints = list(app.blueprints.keys())
        expected = ['auth', 'admin', 'quiz', 'competition']
        
        for bp in expected:
            if bp in blueprints:
                print(f"✓ Blueprint '{bp}' registered")
            else:
                print(f"✗ Blueprint '{bp}' NOT registered")
        
        return all(bp in blueprints for bp in expected)
    except Exception as e:
        print(f"✗ Blueprint test failed: {e}")
        return False

def test_routes(app):
    """Test if key routes exist"""
    print("\nTesting routes...")
    try:
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Home route (/) works")
            else:
                print(f"✗ Home route returned {response.status_code}")
            
            # Test auth routes
            response = client.get('/auth/login')
            if response.status_code == 200:
                print("✓ Login route (/auth/login) works")
            else:
                print(f"✗ Login route returned {response.status_code}")
            
            response = client.get('/auth/register')
            if response.status_code == 200:
                print("✓ Register route (/auth/register) works")
            else:
                print(f"✗ Register route returned {response.status_code}")
            
            # Test quiz route (should redirect if not logged in)
            response = client.get('/quiz/select')
            if response.status_code in [200, 302]:  # 302 is redirect to login
                print("✓ Quiz select route (/quiz/select) accessible")
            else:
                print(f"✗ Quiz select route returned {response.status_code}")
            
            return True
    except Exception as e:
        print(f"✗ Route test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_user(app):
    """Test if admin user exists"""
    print("\nTesting admin user...")
    try:
        with app.app_context():
            from app.models import Role
            admin = User.query.filter_by(role=Role.ADMIN).first()
            if admin:
                print(f"✓ Admin user exists")
                print(f"  - Username: {admin.username}")
                print(f"  - Email: {admin.email}")
                print(f"  - Role: {admin.role}")
                print(f"  - Is Admin: {admin.is_admin()}")
                
                # Check if default admin exists
                default_admin = User.query.filter_by(username='admin').first()
                if default_admin:
                    print(f"  - Default 'admin' user also exists")
                else:
                    print(f"  - Note: Default 'admin' user not found (using custom admin)")
                
                return True
            else:
                print("✗ No admin user found")
                return False
    except Exception as e:
        print(f"✗ Admin user test failed: {e}")
        return False

def test_categories(app):
    """Test if default categories exist"""
    print("\nTesting categories...")
    try:
        with app.app_context():
            categories = Category.query.all()
            if categories:
                print(f"✓ Found {len(categories)} categories:")
                for cat in categories[:5]:  # Show first 5
                    print(f"  - {cat.name}")
                if len(categories) > 5:
                    print(f"  ... and {len(categories) - 5} more")
                return True
            else:
                print("✗ No categories found")
                return False
    except Exception as e:
        print(f"✗ Category test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Flask Quiz Application - Test Suite")
    print("=" * 50)
    
    app = test_app_creation()
    if not app:
        print("\n✗ Cannot proceed without app creation")
        sys.exit(1)
    
    results = []
    results.append(("Database Connection", test_database_connection(app)))
    results.append(("Blueprints", test_blueprints(app)))
    results.append(("Routes", test_routes(app)))
    results.append(("Admin User", test_admin_user(app)))
    results.append(("Categories", test_categories(app)))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Application is working correctly.")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

