# ensure_10_questions_per_difficulty.py
from app import create_app, db
from app.models import Question, Category

app = create_app()

# Generic question templates for each difficulty
question_templates = {
    "Easy": [
        {"text": "What is a basic concept in {category}?", "option1": "Fundamental principle", "option2": "Advanced topic", "option3": "Complex theory", "option4": "Expert level", "correct_option": 1},
        {"text": "Which is the simplest approach in {category}?", "option1": "Basic method", "option2": "Complex method", "option3": "Advanced method", "option4": "Expert method", "correct_option": 1},
        {"text": "What is the primary purpose of {category}?", "option1": "Core functionality", "option2": "Optional feature", "option3": "Advanced feature", "option4": "Expert feature", "correct_option": 1},
        {"text": "Which statement is true about {category} basics?", "option1": "Simple and straightforward", "option2": "Complex and difficult", "option3": "Requires expertise", "option4": "Advanced only", "correct_option": 1},
        {"text": "What is essential to understand {category}?", "option1": "Basic concepts", "option2": "Advanced concepts", "option3": "Expert concepts", "option4": "Complex concepts", "correct_option": 1},
        {"text": "In {category}, what comes first?", "option1": "Fundamentals", "option2": "Advanced topics", "option3": "Expert level", "option4": "Complex topics", "correct_option": 1},
        {"text": "What is the starting point in {category}?", "option1": "Basic introduction", "option2": "Advanced topics", "option3": "Expert knowledge", "option4": "Complex systems", "correct_option": 1},
        {"text": "Which is most important for beginners in {category}?", "option1": "Basic understanding", "option2": "Advanced skills", "option3": "Expert knowledge", "option4": "Complex theories", "correct_option": 1},
        {"text": "What should you learn first in {category}?", "option1": "Basic principles", "option2": "Advanced techniques", "option3": "Expert methods", "option4": "Complex systems", "correct_option": 1},
        {"text": "What is the foundation of {category}?", "option1": "Core basics", "option2": "Advanced concepts", "option3": "Expert knowledge", "option4": "Complex systems", "correct_option": 1}
    ],
    "Medium": [
        {"text": "What is an intermediate concept in {category}?", "option1": "Moderate complexity", "option2": "Very simple", "option3": "Extremely complex", "option4": "Basic only", "correct_option": 1},
        {"text": "Which approach works best at medium level in {category}?", "option1": "Balanced approach", "option2": "Simple approach", "option3": "Complex approach", "option4": "No approach", "correct_option": 1},
        {"text": "What requires moderate understanding in {category}?", "option1": "Intermediate topics", "option2": "Basic topics", "option3": "Expert topics", "option4": "No topics", "correct_option": 1},
        {"text": "Which is a medium-level feature in {category}?", "option1": "Moderate complexity feature", "option2": "Simple feature", "option3": "Expert feature", "option4": "No feature", "correct_option": 1},
        {"text": "What is typical for intermediate {category} users?", "option1": "Moderate skills", "option2": "Basic skills", "option3": "Expert skills", "option4": "No skills", "correct_option": 1},
        {"text": "Which concept is medium-level in {category}?", "option1": "Intermediate concept", "option2": "Basic concept", "option3": "Expert concept", "option4": "No concept", "correct_option": 1},
        {"text": "What is the next step after basics in {category}?", "option1": "Intermediate level", "option2": "Basic level", "option3": "Expert level", "option4": "No level", "correct_option": 1},
        {"text": "Which technique is medium difficulty in {category}?", "option1": "Moderate technique", "option2": "Simple technique", "option3": "Expert technique", "option4": "No technique", "correct_option": 1},
        {"text": "What requires medium knowledge in {category}?", "option1": "Intermediate topics", "option2": "Basic topics", "option3": "Expert topics", "option4": "No topics", "correct_option": 1},
        {"text": "Which is a medium complexity topic in {category}?", "option1": "Moderate topic", "option2": "Simple topic", "option3": "Expert topic", "option4": "No topic", "correct_option": 1}
    ],
    "Hard": [
        {"text": "What is an advanced concept in {category}?", "option1": "Complex principle", "option2": "Simple principle", "option3": "Basic principle", "option4": "No principle", "correct_option": 1},
        {"text": "Which is the most challenging aspect of {category}?", "option1": "Advanced topics", "option2": "Basic topics", "option3": "Simple topics", "option4": "No topics", "correct_option": 1},
        {"text": "What requires expert knowledge in {category}?", "option1": "Complex concepts", "option2": "Basic concepts", "option3": "Simple concepts", "option4": "No concepts", "correct_option": 1},
        {"text": "Which is an expert-level feature in {category}?", "option1": "Advanced feature", "option2": "Basic feature", "option3": "Simple feature", "option4": "No feature", "correct_option": 1},
        {"text": "What is the most complex topic in {category}?", "option1": "Advanced topic", "option2": "Basic topic", "option3": "Simple topic", "option4": "No topic", "correct_option": 1},
        {"text": "Which requires deep understanding in {category}?", "option1": "Expert concepts", "option2": "Basic concepts", "option3": "Simple concepts", "option4": "No concepts", "correct_option": 1},
        {"text": "What is the highest level in {category}?", "option1": "Expert level", "option2": "Basic level", "option3": "Simple level", "option4": "No level", "correct_option": 1},
        {"text": "Which technique is most advanced in {category}?", "option1": "Expert technique", "option2": "Basic technique", "option3": "Simple technique", "option4": "No technique", "correct_option": 1},
        {"text": "What requires mastery in {category}?", "option1": "Advanced topics", "option2": "Basic topics", "option3": "Simple topics", "option4": "No topics", "correct_option": 1},
        {"text": "Which is the most sophisticated concept in {category}?", "option1": "Expert concept", "option2": "Basic concept", "option3": "Simple concept", "option4": "No concept", "correct_option": 1}
    ]
}

with app.app_context():
    print("Ensuring 10 questions per difficulty for each category...")
    
    categories = Category.query.all()
    
    for category in categories:
        cat_name = category.name
        print(f"\nProcessing {cat_name}...")
        
        for difficulty in ["Easy", "Medium", "Hard"]:
            current_count = Question.query.filter_by(
                category_id=category.id,
                difficulty=difficulty
            ).count()
            
            needed = 10 - current_count
            
            if needed > 0:
                print(f"  Adding {needed} {difficulty} questions...")
                templates = question_templates[difficulty]
                
                for i in range(needed):
                    template = templates[i % len(templates)]
                    question = Question(
                        text=template['text'].format(category=cat_name),
                        option1=template['option1'],
                        option2=template['option2'],
                        option3=template['option3'],
                        option4=template['option4'],
                        correct_option=template['correct_option'],
                        difficulty=difficulty,
                        explanation=f"This is a {difficulty.lower()} level question about {cat_name}.",
                        category_id=category.id
                    )
                    db.session.add(question)
                
                db.session.commit()
            elif needed < 0:
                # Too many questions, remove extras
                print(f"  Removing {abs(needed)} extra {difficulty} questions...")
                extra_questions = Question.query.filter_by(
                    category_id=category.id,
                    difficulty=difficulty
                ).limit(abs(needed)).all()
                for q in extra_questions:
                    db.session.delete(q)
                db.session.commit()
            else:
                print(f"  {difficulty}: Already has 10 questions")
    
    print("\n" + "="*50)
    print("Final counts by category and difficulty:")
    print("="*50)
    for category in categories:
        easy = Question.query.filter_by(category_id=category.id, difficulty="Easy").count()
        medium = Question.query.filter_by(category_id=category.id, difficulty="Medium").count()
        hard = Question.query.filter_by(category_id=category.id, difficulty="Hard").count()
        print(f"{category.name}: Easy={easy}, Medium={medium}, Hard={hard}")
    
    print(f"\nTotal questions: {Question.query.count()}")

