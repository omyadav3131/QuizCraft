"""
HEADER_COMMENT_AUTOGEN
FILE: normalize_questions.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from app import create_app, db
from app.models import Question, Category

app = create_app()

with app.app_context():
    print("="*70)
    print("NORMALIZING QUESTIONS - EXACTLY 10 PER DIFFICULTY PER CATEGORY")
    print("="*70)
    
    categories = Category.query.all()
    total_deleted = 0
    
    for category in categories:
        print(f"\n{category.name}:")
        
        for difficulty in ['Easy', 'Medium', 'Hard']:
            questions = Question.query.filter_by(
                category_id=category.id, 
                difficulty=difficulty
            ).order_by(Question.id).all()
            
            current_count = len(questions)
            target_count = 10
            
            if current_count > target_count:
                # Delete extra questions, keeping the first 10
                to_delete = current_count - target_count
                for question in questions[target_count:]:
                    db.session.delete(question)
                    total_deleted += 1
                print(f"  {difficulty}: {current_count} → {target_count} (deleted {to_delete})")
            elif current_count < target_count:
                print(f"  {difficulty}: {current_count} (needs {target_count - current_count} more)")
            else:
                print(f"  {difficulty}: {current_count} ✓ (perfect)")
    
    db.session.commit()
    print(f"\n{'='*70}")
    print(f"Total questions deleted: {total_deleted}")
    print(f"{'='*70}\n")

# Print final verification
with app.app_context():
    print("FINAL VERIFICATION - EXACTLY 10-10-10 REQUIREMENT:")
    print("="*70)
    
    categories = Category.query.all()
    all_perfect = True
    
    for category in sorted(categories, key=lambda x: x.name):
        easy = Question.query.filter_by(category_id=category.id, difficulty='Easy').count()
        medium = Question.query.filter_by(category_id=category.id, difficulty='Medium').count()
        hard = Question.query.filter_by(category_id=category.id, difficulty='Hard').count()
        
        status = "✓" if (easy == 10 and medium == 10 and hard == 10) else "✗"
        print(f"{status} {category.name}: Easy={easy}, Medium={medium}, Hard={hard}")
        
        if easy != 10 or medium != 10 or hard != 10:
            all_perfect = False
    
    print("="*70)
    if all_perfect:
        print("✓ PERFECT! Sab categories me exactly 10-10-10 questions hain")
    else:
        print("✗ Kuch categories abhi incomplete hain")
    print("="*70)
