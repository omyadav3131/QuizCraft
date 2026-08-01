"""
SQLite to PostgreSQL Migration Script for QuizCraft
--------------------------------------------------

Requirements:
1. Ensure `DATABASE_URL` is set to your PostgreSQL database URI.
   Example (Windows PowerShell):
   $env:DATABASE_URL="postgresql://user:password@host:port/dbname"
   
2. Ensure you have installed the required dependencies:
   pip install -r requirements.txt
   
3. Run the script:
   python scripts/migrate_sqlite_to_postgres.py
"""

import os
import sys
import json

# Add parent directory to path so we can import 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from app import create_app, db
from app.models import (
    User, Category, Question, Attempt, AttemptAnswer,
    LeaderboardEntry, Competition, CompetitionAttempt, Feedback
)

def migrate():
    postgres_url = os.environ.get('DATABASE_URL')
    if not postgres_url:
        print("❌ ERROR: DATABASE_URL environment variable is not set.")
        print("Please set it to your PostgreSQL database URI before running.")
        sys.exit(1)
        
    sqlite_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'quiz.db'))
    if not os.path.exists(sqlite_db_path):
        print(f"❌ ERROR: Local database not found at {sqlite_db_path}")
        sys.exit(1)

    print(f"Source: sqlite:///{sqlite_db_path}")
    print(f"Target: {postgres_url.split('@')[-1]}") # Hide credentials
    
    app = create_app()
    with app.app_context():
        # Ensure target schema exists
        print("\nEnsuring target database schema exists...")
        db.create_all()

        # Connect to source SQLite via Core to avoid ORM binding conflicts
        sqlite_engine = create_engine(f'sqlite:///{sqlite_db_path}')

        # Order matters to preserve Foreign Key integrity
        tables_to_migrate = [
            (User, 'user'),
            (Category, 'category'),
            (Question, 'question'),
            (Attempt, 'attempt'),
            (AttemptAnswer, 'attempt_answer'),
            (LeaderboardEntry, 'leaderboard'),
            (Feedback, 'feedback'),
            (Competition, 'competition'),
            (CompetitionAttempt, 'competition_attempt'),
        ]

        total_migrated = 0

        try:
            with sqlite_engine.connect() as conn:
                for model, table_name in tables_to_migrate:
                    print(f"\n--- Migrating table: {table_name} ---")
                    
                    # Fetch all records from SQLite
                    result = conn.execute(text(f"SELECT * FROM {table_name}"))
                    keys = result.keys()
                    rows = result.fetchall()
                    
                    records_count = len(rows)
                    print(f"Found {records_count} records in source.")
                    
                    migrated_for_table = 0
                    
                    for row in rows:
                        row_dict = dict(zip(keys, row))
                        
                        # Data Type Conversions from SQLite raw data
                        if table_name == 'competition_attempt' and 'answers' in row_dict:
                            if isinstance(row_dict['answers'], str):
                                try:
                                    row_dict['answers'] = json.loads(row_dict['answers'])
                                except json.JSONDecodeError:
                                    row_dict['answers'] = {}
                        
                        if table_name == 'attempt_answer' and 'correct' in row_dict:
                            if row_dict['correct'] is not None:
                                row_dict['correct'] = bool(row_dict['correct'])

                        # Idempotent check: Skip if primary key already exists in target
                        pk_val = row_dict['id']
                        exists = db.session.query(model).filter_by(id=pk_val).first()
                        
                        if not exists:
                            new_record = model(**row_dict)
                            db.session.add(new_record)
                            migrated_for_table += 1
                    
                    # Transaction-safe: Commit only after the entire table is staged successfully
                    db.session.commit()
                    print(f"✓ Successfully migrated {migrated_for_table} new records for '{table_name}'.")
                    total_migrated += migrated_for_table
                    
                    # Validation
                    target_count = db.session.query(model).count()
                    print(f"Validation: Source has {records_count}, Target now has {target_count}.")
                    
            print(f"\n======================================")
            print(f"🎉 MIGRATION COMPLETE!")
            print(f"Total new records migrated: {total_migrated}")
            print(f"======================================")
            
            # Reset sequences in PostgreSQL for auto-increment PKs
            # When we explicitly insert IDs, Postgres sequences get out of sync.
            if db.engine.dialect.name == 'postgresql':
                print("\nUpdating PostgreSQL sequences...")
                for model, table_name in tables_to_migrate:
                    try:
                        # Safely update the sequence value to the max ID
                        seq_sql = text(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE((SELECT MAX(id) FROM {table_name}), 1), true)")
                        db.session.execute(seq_sql)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Warning: Could not update sequence for {table_name}: {e}")
                print("✓ Sequences synchronized.")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR during migration: {str(e)}")
            print("Rolled back uncommitted changes to maintain data integrity.")
            sys.exit(1)

if __name__ == '__main__':
    migrate()
