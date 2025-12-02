"""
Script to migrate old Attempt records to LeaderboardEntry
"""
from app import create_app, db
from app.models import Attempt, LeaderboardEntry, User

app = create_app()

with app.app_context():
    print("Migrating old attempts to leaderboard...")
    
    # Get all attempts that don't have a corresponding leaderboard entry
    attempts = Attempt.query.all()
    migrated_count = 0
    skipped_count = 0
    
    for attempt in attempts:
        # Check if user exists
        user = User.query.get(attempt.user_id) if attempt.user_id else None
        username = user.username if user else "Unknown"
        
        # Check if this attempt already exists in leaderboard
        existing = LeaderboardEntry.query.filter_by(
            user_id=attempt.user_id,
            score=attempt.score,
            total=attempt.total,
            category_id=attempt.category_id,
            difficulty=attempt.difficulty,
            created_at=attempt.created_at
        ).first()
        
        if existing:
            skipped_count += 1
            continue
        
        # Create leaderboard entry
        try:
            lb_entry = LeaderboardEntry(
                user_id=attempt.user_id,
                username=username,
                score=attempt.score,
                total=attempt.total,
                category_id=attempt.category_id,
                difficulty=attempt.difficulty,
                created_at=attempt.created_at
            )
            db.session.add(lb_entry)
            migrated_count += 1
        except Exception as e:
            print(f"Error migrating attempt {attempt.id}: {e}")
            db.session.rollback()
            continue
    
    db.session.commit()
    print(f"Migration complete!")
    print(f"Migrated: {migrated_count} attempts")
    print(f"Skipped (already exists): {skipped_count} attempts")

