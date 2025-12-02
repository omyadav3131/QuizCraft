"""
HEADER_COMMENT_AUTOGEN
FILE: update_db.py
PURPOSE: Update existing database with new fields and tables

This script adds:
1. 'points' column to 'attempt' table
2. 'points' column to 'leaderboard' table
3. Creates 'feedback' table

Run this script after making changes to models.py
"""

# update_db.py
from app import create_app, db
from app.models import User, Category, Attempt, LeaderboardEntry, Feedback
import sqlite3
import os

app = create_app()

def update_database():
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        
        # Check if database exists
        if not os.path.exists(db_path):
            print("Database not found. Creating new database...")
            db.create_all()
            print("New database created with all tables!")
            return
        
        print("Updating existing database...")
        
        # Connect to SQLite database directly for ALTER TABLE operations
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check and add 'points' column to 'attempt' table
            cursor.execute("PRAGMA table_info(attempt)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'points' not in columns:
                print("Adding 'points' column to 'attempt' table...")
                cursor.execute("ALTER TABLE attempt ADD COLUMN points INTEGER DEFAULT 0")
                conn.commit()
                print("✓ Added 'points' column to 'attempt' table")
            else:
                print("✓ 'points' column already exists in 'attempt' table")
            
            # Check and add 'points' column to 'leaderboard' table
            cursor.execute("PRAGMA table_info(leaderboard)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'points' not in columns:
                print("Adding 'points' column to 'leaderboard' table...")
                cursor.execute("ALTER TABLE leaderboard ADD COLUMN points INTEGER DEFAULT 0")
                conn.commit()
                print("✓ Added 'points' column to 'leaderboard' table")
            else:
                print("✓ 'points' column already exists in 'leaderboard' table")
            
            # Check if 'feedback' table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
            if not cursor.fetchone():
                print("Creating 'feedback' table...")
                cursor.execute("""
                    CREATE TABLE feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name VARCHAR(150) NOT NULL,
                        rating INTEGER NOT NULL,
                        feedback_text TEXT,
                        created_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES user(id)
                    )
                """)
                conn.commit()
                print("✓ Created 'feedback' table")
            else:
                print("✓ 'feedback' table already exists")
            
            conn.close()
            print("\nDatabase updated successfully!")
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"\nError updating database: {e}")
            print("\nTrying alternative method: dropping and recreating tables...")
            
            # Alternative: recreate all tables using SQLAlchemy
            with app.app_context():
                try:
                    db.drop_all()
                    print("Dropped all tables...")
                    db.create_all()
                    print("Created all tables with new structure!")
                    print("\n⚠ WARNING: All data has been deleted. You may need to recreate categories and admin user.")
                    print("Run 'python create_db.py' to recreate default data.")
                except Exception as e2:
                    print(f"Error in alternative method: {e2}")
                    raise

if __name__ == '__main__':
    update_database()

