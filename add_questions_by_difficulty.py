"""
HEADER_COMMENT_AUTOGEN
FILE: add_questions_by_difficulty.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# add_questions_by_difficulty.py
from app import create_app, db
from app.models import Question, Category

app = create_app()

# Questions organized by category and difficulty
questions_by_difficulty = {
    "C Programming": {
        "Easy": [
            {"text": "What is the size of a char in C?", "option1": "1 byte", "option2": "2 bytes", "option3": "4 bytes", "option4": "8 bytes", "correct_option": 1, "explanation": "A char typically occupies 1 byte of memory."},
            {"text": "Which header file is required for printf()?", "option1": "stdlib.h", "option2": "string.h", "option3": "stdio.h", "option4": "math.h", "correct_option": 3, "explanation": "stdio.h contains the declaration for printf() function."},
            {"text": "What is a pointer in C?", "option1": "A variable that stores address", "option2": "A function", "option3": "A data type", "option4": "A constant", "correct_option": 1, "explanation": "A pointer stores the memory address of another variable."},
            {"text": "What does %d format specifier print?", "option1": "Character", "option2": "Integer", "option3": "Float", "option4": "String", "correct_option": 2, "explanation": "%d is used to print integer values."},
            {"text": "What is the purpose of #include?", "option1": "To include header files", "option2": "To define variables", "option3": "To create functions", "option4": "To print output", "correct_option": 1, "explanation": "#include is used to include header files in C programs."},
            {"text": "What is the default return type of main()?", "option1": "void", "option2": "int", "option3": "char", "option4": "float", "correct_option": 2, "explanation": "The main() function returns int by default."},
            {"text": "What is an array?", "option1": "Collection of similar data types", "option2": "A function", "option3": "A variable", "option4": "A pointer", "correct_option": 1, "explanation": "An array is a collection of elements of the same data type."},
            {"text": "What does strlen() function return?", "option1": "Size of array", "option2": "Length of string", "option3": "Memory address", "option4": "Character count", "correct_option": 2, "explanation": "strlen() returns the length of a string."},
            {"text": "What is the purpose of return statement?", "option1": "To exit function", "option2": "To print value", "option3": "To declare variable", "option4": "To include file", "correct_option": 1, "explanation": "return statement exits a function and optionally returns a value."},
            {"text": "What is a variable in C?", "option1": "A named memory location", "option2": "A function", "option3": "A constant", "option4": "A keyword", "correct_option": 1, "explanation": "A variable is a named memory location that stores data."}
        ],
        "Medium": [
            {"text": "What is the difference between ++i and i++?", "option1": "No difference", "option2": "++i is pre-increment", "option3": "i++ is pre-increment", "option4": "Both invalid", "correct_option": 2, "explanation": "++i increments before use, i++ increments after use."},
            {"text": "What is dynamic memory allocation?", "option1": "Memory allocated at compile time", "option2": "Memory allocated at runtime", "option3": "Static memory", "option4": "Stack memory", "correct_option": 2, "explanation": "Dynamic memory is allocated at runtime using malloc() or calloc()."},
            {"text": "What is a structure in C?", "option1": "A function", "option2": "User-defined data type", "option3": "A variable", "option4": "A pointer", "correct_option": 2, "explanation": "A structure is a user-defined data type that groups related variables."},
            {"text": "What is the purpose of free()?", "option1": "To allocate memory", "option2": "To deallocate memory", "option3": "To initialize memory", "option4": "To clear variables", "correct_option": 2, "explanation": "free() is used to deallocate dynamically allocated memory."},
            {"text": "What is function overloading in C?", "option1": "Supported in C", "option2": "Not supported in C", "option3": "Same as recursion", "option4": "Memory management", "correct_option": 2, "explanation": "Function overloading is not supported in C, only in C++."},
            {"text": "What is a union in C?", "option1": "Similar to structure", "option2": "Shares memory", "option3": "A function", "option4": "A pointer", "correct_option": 2, "explanation": "A union shares memory space among its members."},
            {"text": "What is recursion?", "option1": "Function calling itself", "option2": "Loop structure", "option3": "Memory allocation", "option4": "Pointer operation", "correct_option": 1, "explanation": "Recursion is when a function calls itself."},
            {"text": "What is the difference between array and pointer?", "option1": "Array is constant pointer", "option2": "Pointer is array", "option3": "No difference", "option4": "Both same", "correct_option": 1, "explanation": "An array name is a constant pointer to the first element."},
            {"text": "What is call by value?", "option1": "Passing copy of variable", "option2": "Passing address", "option3": "Passing reference", "option4": "Passing pointer", "correct_option": 1, "explanation": "Call by value passes a copy of the variable to the function."},
            {"text": "What is call by reference?", "option1": "Passing copy", "option2": "Passing address", "option3": "Passing value", "option4": "Passing constant", "correct_option": 2, "explanation": "Call by reference passes the address of the variable."}
        ],
        "Hard": [
            {"text": "What is the output of: int *p; p = malloc(sizeof(int)); *p = 5; printf('%d', *p);", "option1": "5", "option2": "0", "option3": "Error", "option4": "Garbage", "correct_option": 1, "explanation": "The code allocates memory, stores 5, and prints it correctly."},
            {"text": "What is memory leak?", "option1": "Memory not freed", "option2": "Memory allocated", "option3": "Memory cleared", "option4": "Memory used", "correct_option": 1, "explanation": "Memory leak occurs when allocated memory is not freed."},
            {"text": "What is function pointer?", "option1": "Pointer to function", "option2": "Function variable", "option3": "Function call", "option4": "Function name", "correct_option": 1, "explanation": "A function pointer stores the address of a function."},
            {"text": "What is volatile keyword?", "option1": "Prevents optimization", "option2": "Optimizes code", "option3": "Memory modifier", "option4": "Type modifier", "correct_option": 1, "explanation": "volatile tells compiler not to optimize the variable."},
            {"text": "What is const pointer?", "option1": "Pointer that can't change", "option2": "Constant value", "option3": "Variable pointer", "option4": "Mutable pointer", "correct_option": 1, "explanation": "A const pointer cannot be reassigned to point elsewhere."},
            {"text": "What is void pointer?", "option1": "Generic pointer", "option2": "Null pointer", "option3": "Empty pointer", "option4": "Invalid pointer", "correct_option": 1, "explanation": "void* is a generic pointer that can point to any data type."},
            {"text": "What is dangling pointer?", "option1": "Pointer to freed memory", "option2": "Null pointer", "option3": "Valid pointer", "option4": "Initialized pointer", "correct_option": 1, "explanation": "A dangling pointer points to memory that has been freed."},
            {"text": "What is wild pointer?", "option1": "Uninitialized pointer", "option2": "Null pointer", "option3": "Valid pointer", "option4": "Freed pointer", "correct_option": 1, "explanation": "A wild pointer is uninitialized and points to random memory."},
            {"text": "What is pointer arithmetic?", "option1": "Arithmetic on addresses", "option2": "Math operations", "option3": "Variable operations", "option4": "Function calls", "correct_option": 1, "explanation": "Pointer arithmetic involves adding/subtracting integers to pointers."},
            {"text": "What is multi-dimensional array?", "option1": "Array of arrays", "option2": "Single array", "option3": "Pointer array", "option4": "String array", "correct_option": 1, "explanation": "A multi-dimensional array is an array of arrays."}
        ]
    },
    "C++ Programming": {
        "Easy": [
            {"text": "What is the main difference between C and C++?", "option1": "C++ supports OOP", "option2": "C++ is faster", "option3": "No difference", "option4": "C++ has no pointers", "correct_option": 1, "explanation": "C++ supports object-oriented programming features."},
            {"text": "What is a class in C++?", "option1": "A function", "option2": "Blueprint for objects", "option3": "A variable", "option4": "A library", "correct_option": 2, "explanation": "A class is a blueprint for creating objects."},
            {"text": "What is the purpose of 'new' keyword?", "option1": "Create variable", "option2": "Allocate memory", "option3": "Delete memory", "option4": "Initialize array", "correct_option": 2, "explanation": "'new' operator allocates memory dynamically."},
            {"text": "What is a constructor?", "option1": "Destroys objects", "option2": "Initializes objects", "option3": "A variable", "option4": "A function", "correct_option": 2, "explanation": "Constructor initializes objects when created."},
            {"text": "What is public access modifier?", "option1": "Accessible everywhere", "option2": "Private access", "option3": "Protected only", "option4": "No access", "correct_option": 1, "explanation": "Public members are accessible from outside the class."},
            {"text": "What is private access modifier?", "option1": "Accessible everywhere", "option2": "Only within class", "option3": "Public access", "option4": "No restrictions", "correct_option": 2, "explanation": "Private members are only accessible within the class."},
            {"text": "What is inheritance?", "option1": "Creating new classes", "option2": "Reusing existing classes", "option3": "Deleting classes", "option4": "Copying classes", "correct_option": 2, "explanation": "Inheritance allows reusing code from existing classes."},
            {"text": "What is a destructor?", "option1": "Creates objects", "option2": "Cleans up objects", "option3": "A constructor", "option4": "A variable", "correct_option": 2, "explanation": "Destructor cleans up when object is destroyed."},
            {"text": "What is function overloading?", "option1": "Same name, different parameters", "option2": "Different names", "option3": "Same parameters", "option4": "No functions", "correct_option": 1, "explanation": "Function overloading allows same name with different parameters."},
            {"text": "What is namespace in C++?", "option1": "Container for identifiers", "option2": "A class", "option3": "A function", "option4": "A variable", "correct_option": 1, "explanation": "Namespace groups related identifiers together."}
        ],
        "Medium": [
            {"text": "What is encapsulation?", "option1": "Hiding data and methods", "option2": "Inheriting classes", "option3": "Using pointers", "option4": "Memory management", "correct_option": 1, "explanation": "Encapsulation bundles data and methods together."},
            {"text": "What is polymorphism?", "option1": "Multiple forms", "option2": "Single form", "option3": "Memory allocation", "option4": "Variable types", "correct_option": 1, "explanation": "Polymorphism allows objects of different types through same interface."},
            {"text": "What is virtual function?", "option1": "Function that can be overridden", "option2": "Real function", "option3": "Static function", "option4": "Inline function", "correct_option": 1, "explanation": "Virtual function enables runtime polymorphism."},
            {"text": "What is abstract class?", "option1": "Cannot be instantiated", "option2": "Can be instantiated", "option3": "Concrete class", "option4": "Final class", "correct_option": 1, "explanation": "Abstract class has at least one pure virtual function."},
            {"text": "What is operator overloading?", "option1": "Redefining operators", "option2": "Creating operators", "option3": "Deleting operators", "option4": "Using operators", "correct_option": 1, "explanation": "Operator overloading redefines operators for user types."},
            {"text": "What is template in C++?", "option1": "Generic programming", "option2": "Specific programming", "option3": "Function only", "option4": "Class only", "correct_option": 1, "explanation": "Templates enable generic programming with type parameters."},
            {"text": "What is STL?", "option1": "Standard Template Library", "option2": "Simple Template Library", "option3": "System Template Library", "option4": "String Template Library", "correct_option": 1, "explanation": "STL provides containers, algorithms, and iterators."},
            {"text": "What is exception handling?", "option1": "Managing errors", "option2": "Creating errors", "option3": "Ignoring errors", "option4": "Preventing compilation", "correct_option": 1, "explanation": "Exception handling manages runtime errors gracefully."},
            {"text": "What is friend function?", "option1": "Accesses private members", "option2": "Public function", "option3": "Private function", "option4": "Protected function", "correct_option": 1, "explanation": "Friend function can access private members of a class."},
            {"text": "What is multiple inheritance?", "option1": "Inheriting from multiple classes", "option2": "Single inheritance", "option3": "No inheritance", "option4": "Partial inheritance", "correct_option": 1, "explanation": "Multiple inheritance allows a class to inherit from multiple base classes."}
        ],
        "Hard": [
            {"text": "What is diamond problem?", "option1": "Multiple inheritance ambiguity", "option2": "Single inheritance", "option3": "No inheritance", "option4": "Virtual inheritance", "correct_option": 1, "explanation": "Diamond problem occurs in multiple inheritance with common base."},
            {"text": "What is RAII?", "option1": "Resource Acquisition Is Initialization", "option2": "Random Access", "option3": "Resource Allocation", "option4": "Runtime Allocation", "correct_option": 1, "explanation": "RAII binds resource lifecycle to object lifetime."},
            {"text": "What is move semantics?", "option1": "Efficient resource transfer", "option2": "Copy semantics", "option3": "Reference semantics", "option4": "Value semantics", "correct_option": 1, "explanation": "Move semantics transfers resources without copying."},
            {"text": "What is smart pointer?", "option1": "Automatic memory management", "option2": "Raw pointer", "option3": "Null pointer", "option4": "Void pointer", "correct_option": 1, "explanation": "Smart pointers automatically manage memory (unique_ptr, shared_ptr)."},
            {"text": "What is lambda expression?", "option1": "Anonymous function", "option2": "Named function", "option3": "Class method", "option4": "Global function", "correct_option": 1, "explanation": "Lambda is an anonymous function object."},
            {"text": "What is constexpr?", "option1": "Compile-time constant", "option2": "Runtime constant", "option3": "Variable", "option4": "Function", "correct_option": 1, "explanation": "constexpr evaluates at compile time."},
            {"text": "What is variadic template?", "option1": "Template with variable arguments", "option2": "Fixed template", "option3": "Single template", "option4": "No template", "correct_option": 1, "explanation": "Variadic templates accept variable number of arguments."},
            {"text": "What is perfect forwarding?", "option1": "Preserving value category", "option2": "Changing value", "option3": "Copying value", "option4": "Moving value", "correct_option": 1, "explanation": "Perfect forwarding preserves lvalue/rvalue nature."},
            {"text": "What is CRTP?", "option1": "Curiously Recurring Template Pattern", "option2": "Class Recurring", "option3": "Compile Recurring", "option4": "Code Recurring", "correct_option": 1, "explanation": "CRTP is a template pattern for static polymorphism."},
            {"text": "What is SFINAE?", "option1": "Substitution Failure Is Not An Error", "option2": "Syntax Failure", "option3": "Semantic Failure", "option4": "System Failure", "correct_option": 1, "explanation": "SFINAE allows template substitution failures without errors."}
        ]
    }
}

# Add more categories with similar structure - I'll create a simplified version
categories_list = [
    "Data Structures", "General Knowledge", "Java Programming", 
    "Logical Reasoning", "Python Programming", "Quantitative Aptitude", "SQL"
]

with app.app_context():
    print("Adding questions by difficulty level...")
    
    # Add questions for C Programming and C++ (already defined)
    for cat_name, difficulties in questions_by_difficulty.items():
        category = Category.query.filter_by(name=cat_name).first()
        if not category:
            continue
            
        for difficulty, questions in difficulties.items():
            added = 0
            for q_data in questions:
                existing = Question.query.filter_by(
                    text=q_data['text'],
                    category_id=category.id,
                    difficulty=difficulty
                ).first()
                if not existing:
                    question = Question(
                        text=q_data['text'],
                        option1=q_data['option1'],
                        option2=q_data['option2'],
                        option3=q_data.get('option3', ''),
                        option4=q_data.get('option4', ''),
                        correct_option=q_data['correct_option'],
                        difficulty=difficulty,
                        explanation=q_data.get('explanation', ''),
                        category_id=category.id
                    )
                    db.session.add(question)
                    added += 1
            db.session.commit()
            print(f"Added {added} {difficulty} questions for {cat_name}")
    
    # For other categories, we'll update existing questions or add new ones
    # Let's update existing questions to have proper difficulty distribution
    for cat_name in categories_list:
        category = Category.query.filter_by(name=cat_name).first()
        if not category:
            continue
        
        # Get existing questions
        existing_questions = Question.query.filter_by(category_id=category.id).all()
        
        # Distribute them across difficulties (if we have 30, make 10 each)
        if len(existing_questions) >= 10:
            for i, q in enumerate(existing_questions[:10]):
                q.difficulty = "Easy"
            for i, q in enumerate(existing_questions[10:20]):
                if i < len(existing_questions) - 10:
                    q.difficulty = "Medium"
            for i, q in enumerate(existing_questions[20:30]):
                if i < len(existing_questions) - 20:
                    q.difficulty = "Hard"
            db.session.commit()
            print(f"Updated difficulty levels for {cat_name}")
    
    print("\nQuestions by difficulty added successfully!")
    print(f"Total questions: {Question.query.count()}")

