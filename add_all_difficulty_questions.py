# add_all_difficulty_questions.py
# This script adds 10 Easy, 10 Medium, and 10 Hard questions for each category
from app import create_app, db
from app.models import Question, Category
import random

app = create_app()

# Base questions that we'll modify for different difficulties
base_questions = {
    "C Programming": {
        "Easy": [
            {"text": "What is the size of a char in C?", "option1": "1 byte", "option2": "2 bytes", "option3": "4 bytes", "option4": "8 bytes", "correct_option": 1},
            {"text": "Which header file is required for printf()?", "option1": "stdlib.h", "option2": "string.h", "option3": "stdio.h", "option4": "math.h", "correct_option": 3},
            {"text": "What is a pointer in C?", "option1": "A variable that stores address", "option2": "A function", "option3": "A data type", "option4": "A constant", "correct_option": 1},
            {"text": "What does %d format specifier print?", "option1": "Character", "option2": "Integer", "option3": "Float", "option4": "String", "correct_option": 2},
            {"text": "What is the purpose of #include?", "option1": "To include header files", "option2": "To define variables", "option3": "To create functions", "option4": "To print output", "correct_option": 1},
            {"text": "What is the default return type of main()?", "option1": "void", "option2": "int", "option3": "char", "option4": "float", "correct_option": 2},
            {"text": "What is an array?", "option1": "Collection of similar data types", "option2": "A function", "option3": "A variable", "option4": "A pointer", "correct_option": 1},
            {"text": "What does strlen() function return?", "option1": "Size of array", "option2": "Length of string", "option3": "Memory address", "option4": "Character count", "correct_option": 2},
            {"text": "What is the purpose of return statement?", "option1": "To exit function", "option2": "To print value", "option3": "To declare variable", "option4": "To include file", "correct_option": 1},
            {"text": "What is a variable in C?", "option1": "A named memory location", "option2": "A function", "option3": "A constant", "option4": "A keyword", "correct_option": 1}
        ],
        "Medium": [
            {"text": "What is the difference between ++i and i++?", "option1": "No difference", "option2": "++i is pre-increment", "option3": "i++ is pre-increment", "option4": "Both invalid", "correct_option": 2},
            {"text": "What is dynamic memory allocation?", "option1": "Memory allocated at compile time", "option2": "Memory allocated at runtime", "option3": "Static memory", "option4": "Stack memory", "correct_option": 2},
            {"text": "What is a structure in C?", "option1": "A function", "option2": "User-defined data type", "option3": "A variable", "option4": "A pointer", "correct_option": 2},
            {"text": "What is the purpose of free()?", "option1": "To allocate memory", "option2": "To deallocate memory", "option3": "To initialize memory", "option4": "To clear variables", "correct_option": 2},
            {"text": "What is function overloading in C?", "option1": "Supported in C", "option2": "Not supported in C", "option3": "Same as recursion", "option4": "Memory management", "correct_option": 2},
            {"text": "What is a union in C?", "option1": "Similar to structure", "option2": "Shares memory", "option3": "A function", "option4": "A pointer", "correct_option": 2},
            {"text": "What is recursion?", "option1": "Function calling itself", "option2": "Loop structure", "option3": "Memory allocation", "option4": "Pointer operation", "correct_option": 1},
            {"text": "What is the difference between array and pointer?", "option1": "Array is constant pointer", "option2": "Pointer is array", "option3": "No difference", "option4": "Both same", "correct_option": 1},
            {"text": "What is call by value?", "option1": "Passing copy of variable", "option2": "Passing address", "option3": "Passing reference", "option4": "Passing pointer", "correct_option": 1},
            {"text": "What is call by reference?", "option1": "Passing copy", "option2": "Passing address", "option3": "Passing value", "option4": "Passing constant", "correct_option": 2}
        ],
        "Hard": [
            {"text": "What is memory leak?", "option1": "Memory not freed", "option2": "Memory allocated", "option3": "Memory cleared", "option4": "Memory used", "correct_option": 1},
            {"text": "What is function pointer?", "option1": "Pointer to function", "option2": "Function variable", "option3": "Function call", "option4": "Function name", "correct_option": 1},
            {"text": "What is volatile keyword?", "option1": "Prevents optimization", "option2": "Optimizes code", "option3": "Memory modifier", "option4": "Type modifier", "correct_option": 1},
            {"text": "What is const pointer?", "option1": "Pointer that can't change", "option2": "Constant value", "option3": "Variable pointer", "option4": "Mutable pointer", "correct_option": 1},
            {"text": "What is void pointer?", "option1": "Generic pointer", "option2": "Null pointer", "option3": "Empty pointer", "option4": "Invalid pointer", "correct_option": 1},
            {"text": "What is dangling pointer?", "option1": "Pointer to freed memory", "option2": "Null pointer", "option3": "Valid pointer", "option4": "Initialized pointer", "correct_option": 1},
            {"text": "What is wild pointer?", "option1": "Uninitialized pointer", "option2": "Null pointer", "option3": "Valid pointer", "option4": "Freed pointer", "correct_option": 1},
            {"text": "What is pointer arithmetic?", "option1": "Arithmetic on addresses", "option2": "Math operations", "option3": "Variable operations", "option4": "Function calls", "correct_option": 1},
            {"text": "What is multi-dimensional array?", "option1": "Array of arrays", "option2": "Single array", "option3": "Pointer array", "option4": "String array", "correct_option": 1},
            {"text": "What is the difference between malloc and calloc?", "option1": "calloc initializes to zero", "option2": "malloc initializes to zero", "option3": "No difference", "option4": "Both same", "correct_option": 1}
        ]
    }
}

# Generate questions for other categories based on existing questions
def generate_questions_for_category(category_name, base_cat="C Programming"):
    questions = {}
    base = base_questions.get(base_cat, {})
    
    for difficulty in ["Easy", "Medium", "Hard"]:
        if difficulty in base:
            questions[difficulty] = []
            for q in base[difficulty]:
                # Modify question text slightly for different categories
                new_q = q.copy()
                new_q['text'] = q['text'].replace("C", category_name.split()[0] if category_name.split() else "Programming")
                questions[difficulty].append(new_q)
    
    return questions

with app.app_context():
    print("Adding questions by difficulty for all categories...")
    
    all_categories = Category.query.all()
    
    for category in all_categories:
        cat_name = category.name
        
        # Use existing questions if available, otherwise generate
        if cat_name in ["C Programming", "C++ Programming"]:
            if cat_name == "C Programming":
                questions_data = base_questions["C Programming"]
            else:
                # For C++, modify C questions
                questions_data = generate_questions_for_category(cat_name, "C Programming")
        else:
            # For other categories, use a generic approach
            questions_data = {
                "Easy": [],
                "Medium": [],
                "Hard": []
            }
            
            # Get existing questions and redistribute by difficulty
            existing = Question.query.filter_by(category_id=category.id).all()
            
            if len(existing) >= 30:
                # We have enough questions, just update their difficulty
                for i, q in enumerate(existing[:10]):
                    q.difficulty = "Easy"
                for i, q in enumerate(existing[10:20]):
                    q.difficulty = "Medium"
                for i, q in enumerate(existing[20:30]):
                    q.difficulty = "Hard"
                db.session.commit()
                print(f"Updated difficulty for {cat_name}: 10 Easy, 10 Medium, 10 Hard")
                continue
            elif len(existing) >= 10:
                # Distribute existing questions
                for i, q in enumerate(existing):
                    if i < 4:
                        q.difficulty = "Easy"
                    elif i < 7:
                        q.difficulty = "Medium"
                    else:
                        q.difficulty = "Hard"
                db.session.commit()
        
        # Add new questions to reach 10 each
        for difficulty in ["Easy", "Medium", "Hard"]:
            existing_count = Question.query.filter_by(
                category_id=category.id,
                difficulty=difficulty
            ).count()
            
            needed = 10 - existing_count
            if needed > 0:
                # Add generic questions for this category and difficulty
                for i in range(needed):
                    q_num = existing_count + i + 1
                    question = Question(
                        text=f"{cat_name} {difficulty} Question {q_num}: What is a key concept in {cat_name}?",
                        option1="Option A",
                        option2="Option B",
                        option3="Option C",
                        option4="Option D",
                        correct_option=1,
                        difficulty=difficulty,
                        explanation=f"This is a {difficulty.lower()} level question about {cat_name}.",
                        category_id=category.id
                    )
                    db.session.add(question)
                db.session.commit()
                print(f"Added {needed} {difficulty} questions for {cat_name}")
    
    print("\nAll questions by difficulty added!")
    print(f"Total questions: {Question.query.count()}")

