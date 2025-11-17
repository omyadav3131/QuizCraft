"""
HEADER_COMMENT_AUTOGEN
FILE: fix_cpp_questions.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from app import create_app, db
from app.models import Question, Category

app = create_app()

cpp_questions = {
    'Medium': [
        {
            'text': 'What is the primary difference between new and malloc in C++?',
            'options': [
                'new is type-safe, malloc is not',
                'new calls constructor, malloc does not',
                'Both A and B',
                'There is no difference'
            ],
            'correct': 3,
            'explanation': 'new is type-safe and calls constructors, while malloc is just memory allocation without type checking or constructor calls.'
        },
        {
            'text': 'What does RAII stand for in C++?',
            'options': [
                'Resource Allocation Is Instantiation',
                'Resource Allocation in Implementation',
                'Reference Allocation Is Important',
                'Resource Assignment Is Instant'
            ],
            'correct': 1,
            'explanation': 'RAII (Resource Acquisition Is Initialization) ties resource management to object lifetime.'
        },
        {
            'text': 'Which of the following is NOT a type of smart pointer in C++11?',
            'options': [
                'unique_ptr',
                'shared_ptr',
                'weak_ptr',
                'strong_ptr'
            ],
            'correct': 4,
            'explanation': 'strong_ptr does not exist in C++. The main smart pointers are unique_ptr, shared_ptr, and weak_ptr.'
        },
        {
            'text': 'What is the purpose of the mutable keyword in C++?',
            'options': [
                'To allow modification of const member variables',
                'To prevent modification of variables',
                'To declare abstract methods',
                'To declare virtual functions'
            ],
            'correct': 1,
            'explanation': 'mutable allows const member functions to modify specific member variables.'
        },
        {
            'text': 'How many times is the destructor called for a temporary object?',
            'options': [
                'Never',
                'Once at the end of the expression',
                'Twice - when created and destroyed',
                'It depends on the compiler'
            ],
            'correct': 2,
            'explanation': 'The destructor is called once at the end of the full expression containing the temporary object.'
        },
        {
            'text': 'What is the difference between struct and class in C++?',
            'options': [
                'No functional difference',
                'struct members are public by default, class members are private',
                'struct cannot have functions',
                'class cannot have inheritance'
            ],
            'correct': 2,
            'explanation': 'The main difference is member access: struct defaults to public, class defaults to private.'
        }
    ],
    'Hard': [
        {
            'text': 'What is the output of this code? int* p = new int[5]; delete p;',
            'options': [
                'Undefined behavior - should use delete[]',
                'Compiles and runs fine',
                'Compile error',
                'Runtime error always'
            ],
            'correct': 1,
            'explanation': 'Using delete instead of delete[] on array pointers causes undefined behavior - likely memory leak.'
        },
        {
            'text': 'In C++, what is the difference between static_cast and reinterpret_cast?',
            'options': [
                'static_cast is type-safe, reinterpret_cast is not',
                'Both are identical',
                'reinterpret_cast is for inheritance hierarchies',
                'static_cast is only for pointers'
            ],
            'correct': 1,
            'explanation': 'static_cast performs safe conversions with compiler checks, reinterpret_cast does raw bit reinterpretation without safety checks.'
        },
        {
            'text': 'What is the purpose of the volatile keyword in C++?',
            'options': [
                'To prevent optimization of a variable',
                'To make a variable immutable',
                'To declare thread-safe variables',
                'To allocate variables on the stack'
            ],
            'correct': 1,
            'explanation': 'volatile tells the compiler not to optimize away accesses to a variable, useful for memory-mapped I/O.'
        },
        {
            'text': 'Which of these correctly demonstrates move semantics in C++?',
            'options': [
                'std::vector<int> v1 = v2;',
                'std::vector<int> v1 = std::move(v2);',
                'std::vector<int> v1 &= v2;',
                'std::vector<int> v1 <<= v2;'
            ],
            'correct': 2,
            'explanation': 'std::move() enables move semantics, allowing efficient transfer of resources.'
        },
        {
            'text': 'What does the pimpl (Pointer to Implementation) idiom provide?',
            'options': [
                'Faster compilation and reduced coupling',
                'Better runtime performance',
                'Automatic memory management',
                'Thread safety'
            ],
            'correct': 1,
            'explanation': 'Pimpl hides implementation details, reduces compilation dependencies, and allows changing implementation without affecting interface.'
        },
        {
            'text': 'In template metaprogramming, what is SFINAE?',
            'options': [
                'Substitution Failure Is Not An Error',
                'Static Function Name Is Ambiguous',
                'Secure Function Naming And Interface',
                'Simultaneous Functional And Numerical Execution'
            ],
            'correct': 1,
            'explanation': 'SFINAE is a C++ template technique where template substitution failures don\'t cause compiler errors.'
        }
    ]
}

with app.app_context():
    category = Category.query.filter_by(name='C++ Programming').first()
    
    added_count = 0
    for difficulty, questions_list in cpp_questions.items():
        for q_data in questions_list:
            # Check if question already exists
            if not Question.query.filter_by(text=q_data['text'], category_id=category.id).first():
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
                added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} new C++ questions")

# Print final stats
with app.app_context():
    print("\n" + "="*60)
    print("FINAL C++ PROGRAMMING STATS:")
    print("="*60)
    
    category_id = Category.query.filter_by(name='C++ Programming').first().id
    
    for difficulty in ['Easy', 'Medium', 'Hard']:
        count = Question.query.filter_by(category_id=category_id, difficulty=difficulty).count()
        print(f"{difficulty}: {count} questions")
    
    total = Question.query.filter_by(category_id=category_id).count()
    print(f"TOTAL: {total} questions")
