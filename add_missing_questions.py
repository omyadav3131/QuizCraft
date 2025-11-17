"""
HEADER_COMMENT_AUTOGEN
FILE: add_missing_questions.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from app import create_app, db
from app.models import Question, Category

app = create_app()

questions_to_add = {
    'C++ Programming': {
        'Hard': [
            {
                'text': 'Which C++ feature allows defining multiple functions with the same name but different parameters?',
                'options': ['Operator Overloading', 'Function Overloading', 'Function Shadowing', 'Template Specialization'],
                'correct': 2,
                'explanation': 'Function overloading allows multiple functions with the same name but different parameter lists.'
            },
            {
                'text': 'What is the purpose of the constexpr keyword introduced in C++11?',
                'options': ['Define constant expressions that can be evaluated at compile-time', 'Declare thread-safe constants', 'Define immutable class members', 'Mark functions as non-modifiable'],
                'correct': 1,
                'explanation': 'constexpr enables compile-time evaluation of constant expressions, improving performance.'
            },
            {
                'text': 'In C++, what is the difference between std::vector and std::array?',
                'options': ['array has fixed size, vector has dynamic size', 'vector is faster than array', 'array supports more operations', 'No significant difference'],
                'correct': 1,
                'explanation': 'std::array has compile-time fixed size and is allocated on stack, std::vector has dynamic size and is allocated on heap.'
            }
        ]
    },
    'General Knowledge': {
        'Medium': [
            {
                'text': 'Which planet is known as the "Red Planet"?',
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'correct': 2,
                'explanation': 'Mars is known as the Red Planet due to its reddish appearance caused by iron oxide (rust) on its surface.'
            },
            {
                'text': 'Who was the first President of the United States?',
                'options': ['Thomas Jefferson', 'George Washington', 'John Adams', 'Benjamin Franklin'],
                'correct': 2,
                'explanation': 'George Washington was the first President of the United States, serving from 1789 to 1797.'
            },
            {
                'text': 'What is the capital of France?',
                'options': ['Lyon', 'Paris', 'Marseille', 'Nice'],
                'correct': 2,
                'explanation': 'Paris is the capital and largest city of France, known as the "City of Light".'
            }
        ]
    },
    'SQL': {
        'Medium': [
            {
                'text': 'Which SQL clause is used to filter groups based on aggregate functions?',
                'options': ['WHERE', 'GROUP BY', 'HAVING', 'ORDER BY'],
                'correct': 3,
                'explanation': 'HAVING clause is used to filter groups created by GROUP BY, similar to WHERE for aggregate functions.'
            },
            {
                'text': 'What does ACID stand for in database transactions?',
                'options': ['Atomicity, Consistency, Isolation, Durability', 'Atomicity, Concurrency, Isolation, Durability', 'Accessibility, Consistency, Integration, Durability', 'None of the above'],
                'correct': 1,
                'explanation': 'ACID properties ensure reliable database transactions: Atomicity (all or nothing), Consistency (valid state), Isolation (independent), Durability (permanent).'
            }
        ]
    }
}

with app.app_context():
    print("="*70)
    print("ADDING MISSING QUESTIONS TO COMPLETE 10-10-10")
    print("="*70)
    
    total_added = 0
    
    for category_name, difficulties in questions_to_add.items():
        print(f"\n{category_name}:")
        category = Category.query.filter_by(name=category_name).first()
        
        for difficulty, questions_list in difficulties.items():
            for q_data in questions_list:
                question = Question(
                    text=q_data['text'],
                    option1=q_data['options'][0],
                    option2=q_data['options'][1],
                    option3=q_data['options'][2],
                    option4=q_data['options'][3],
                    correct_option=q_data['correct'],
                    explanation=q_data['explanation'],
                    difficulty=difficulty,
                    category_id=category.id
                )
                db.session.add(question)
                total_added += 1
            
            print(f"  {difficulty}: Added {len(questions_list)} questions")
    
    db.session.commit()
    print(f"\n{'='*70}")
    print(f"Total questions added: {total_added}")
    print(f"{'='*70}\n")

# Final verification
with app.app_context():
    print("FINAL VERIFICATION - EXACTLY 10-10-10:")
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
        print("✓✓✓ PERFECT! Sab 9 categories me EXACTLY 10-10-10 questions hain!")
        print("✓✓✓ Total: 270 questions (9 categories × 30 questions)")
    else:
        print("✗ Abhi kuch incomplete hain")
    print("="*70)
