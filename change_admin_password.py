"""
Script to change admin password directly in the database
Usage: python change_admin_password.py
"""

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        print("❌ Admin user not found!")
        exit(1)
    
    print(f"Current admin user: {admin.username}")
    print(f"Current email: {admin.email}")
    
    # Get new password
    new_password = input("\nEnter new password for admin: ")
    confirm_password = input("Confirm new password: ")
    
    if new_password != confirm_password:
        print("❌ Passwords do not match!")
        exit(1)
    
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters long!")
        exit(1)
    
    # Update password
    admin.set_password(new_password)
    db.session.commit()
    
    print("\n✅ Admin password changed successfully!")
    print(f"Username: {admin.username}")
    print(f"New password: {new_password}")

