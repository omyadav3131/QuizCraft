"""
HEADER_COMMENT_AUTOGEN
FILE: add_sample_questions.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# add_sample_questions.py
from app import create_app, db
from app.models import Question, Category

app = create_app()

# Sample questions for each category
questions_data = {
    "C Programming": [
        {
            "text": "What is the output of printf('%d', sizeof(int))?",
            "option1": "2",
            "option2": "4",
            "option3": "8",
            "option4": "Depends on compiler",
            "correct_option": 4,
            "difficulty": "Medium",
            "explanation": "Size of int depends on the compiler and system architecture."
        },
        {
            "text": "Which of the following is not a valid C variable name?",
            "option1": "int_var",
            "option2": "var_name",
            "option3": "2var",
            "option4": "_var",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "Variable names cannot start with a digit."
        },
        {
            "text": "What is the purpose of malloc() in C?",
            "option1": "To free memory",
            "option2": "To allocate memory dynamically",
            "option3": "To initialize variables",
            "option4": "To print output",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "malloc() is used to allocate memory dynamically at runtime."
        },
        {
            "text": "What does the '&' operator do in C?",
            "option1": "Logical AND",
            "option2": "Address of operator",
            "option3": "Bitwise AND",
            "option4": "Assignment operator",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "& is the address-of operator that returns the memory address of a variable."
        },
        {
            "text": "Which header file is required for printf()?",
            "option1": "stdlib.h",
            "option2": "string.h",
            "option3": "stdio.h",
            "option4": "math.h",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "stdio.h contains the declaration for printf() function."
        },
        {
            "text": "What is a pointer in C?",
            "option1": "A variable that stores address of another variable",
            "option2": "A function",
            "option3": "A data type",
            "option4": "A constant",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A pointer is a variable that stores the memory address of another variable."
        },
        {
            "text": "What is the difference between ++i and i++?",
            "option1": "No difference",
            "option2": "++i is pre-increment, i++ is post-increment",
            "option3": "++i is post-increment, i++ is pre-increment",
            "option4": "Both are invalid",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "++i increments before use, i++ increments after use."
        },
        {
            "text": "Which function is used to read a string in C?",
            "option1": "scanf()",
            "option2": "gets()",
            "option3": "fgets()",
            "option4": "All of the above",
            "correct_option": 4,
            "difficulty": "Medium",
            "explanation": "All three functions can be used, but fgets() is safer than gets()."
        },
        {
            "text": "What is the size of a char in C?",
            "option1": "1 byte",
            "option2": "2 bytes",
            "option3": "4 bytes",
            "option4": "8 bytes",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A char typically occupies 1 byte of memory."
        },
        {
            "text": "What is the purpose of free() in C?",
            "option1": "To allocate memory",
            "option2": "To deallocate dynamically allocated memory",
            "option3": "To initialize memory",
            "option4": "To clear variables",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "free() is used to deallocate memory that was allocated using malloc(), calloc(), or realloc()."
        }
    ],
    "C++ Programming": [
        {
            "text": "What is the main difference between C and C++?",
            "option1": "C++ supports object-oriented programming",
            "option2": "C++ is faster",
            "option3": "C++ has no pointers",
            "option4": "No difference",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "C++ supports OOP features like classes, inheritance, and polymorphism."
        },
        {
            "text": "What is a class in C++?",
            "option1": "A function",
            "option2": "A blueprint for creating objects",
            "option3": "A variable",
            "option4": "A library",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "A class is a user-defined data type that serves as a blueprint for creating objects."
        },
        {
            "text": "What is encapsulation in C++?",
            "option1": "Hiding data and methods within a class",
            "option2": "Inheriting from multiple classes",
            "option3": "Using pointers",
            "option4": "Memory management",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "Encapsulation is the bundling of data and methods that operate on that data within a single unit."
        },
        {
            "text": "What is the purpose of 'new' keyword in C++?",
            "option1": "To create a new variable",
            "option2": "To allocate memory dynamically",
            "option3": "To delete memory",
            "option4": "To initialize arrays",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "The 'new' operator is used to dynamically allocate memory for objects."
        },
        {
            "text": "What is inheritance in C++?",
            "option1": "Creating new classes from existing classes",
            "option2": "Memory allocation",
            "option3": "Function overloading",
            "option4": "Variable declaration",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "Inheritance allows a class to inherit properties and methods from another class."
        },
        {
            "text": "What is function overloading?",
            "option1": "Having multiple functions with same name but different parameters",
            "option2": "Having functions with different names",
            "option3": "Calling functions multiple times",
            "option4": "Deleting functions",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "Function overloading allows multiple functions with the same name but different parameters."
        },
        {
            "text": "What is a constructor in C++?",
            "option1": "A function that destroys objects",
            "option2": "A special function that initializes objects",
            "option3": "A variable",
            "option4": "A library function",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "A constructor is a special member function that initializes objects when they are created."
        },
        {
            "text": "What is polymorphism in C++?",
            "option1": "Having multiple forms",
            "option2": "Single form only",
            "option3": "Memory management",
            "option4": "Variable types",
            "correct_option": 1,
            "difficulty": "Hard",
            "explanation": "Polymorphism allows objects of different types to be accessed through the same interface."
        },
        {
            "text": "What is the difference between public and private in C++?",
            "option1": "Public is accessible everywhere, private only within class",
            "option2": "No difference",
            "option3": "Private is accessible everywhere",
            "option4": "Both are same",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "Public members are accessible from outside the class, private members are only accessible within the class."
        },
        {
            "text": "What is a destructor in C++?",
            "option1": "A function that creates objects",
            "option2": "A special function that cleans up when object is destroyed",
            "option3": "A constructor",
            "option4": "A variable",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "A destructor is a special member function that is called when an object is destroyed."
        }
    ],
    "Data Structures": [
        {
            "text": "What is the time complexity of accessing an element in an array?",
            "option1": "O(1)",
            "option2": "O(n)",
            "option3": "O(log n)",
            "option4": "O(n²)",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "Array access is O(1) because elements are stored in contiguous memory locations."
        },
        {
            "text": "What is a stack?",
            "option1": "LIFO data structure",
            "option2": "FIFO data structure",
            "option3": "Random access structure",
            "option4": "Tree structure",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "Stack follows Last In First Out (LIFO) principle."
        },
        {
            "text": "What is a queue?",
            "option1": "LIFO data structure",
            "option2": "FIFO data structure",
            "option3": "Random access",
            "option4": "Tree structure",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Queue follows First In First Out (FIFO) principle."
        },
        {
            "text": "What is the time complexity of binary search?",
            "option1": "O(1)",
            "option2": "O(n)",
            "option3": "O(log n)",
            "option4": "O(n²)",
            "correct_option": 3,
            "difficulty": "Medium",
            "explanation": "Binary search divides the search space in half each time, resulting in O(log n) complexity."
        },
        {
            "text": "What is a linked list?",
            "option1": "A collection of nodes connected by pointers",
            "option2": "An array",
            "option3": "A stack",
            "option4": "A queue",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A linked list is a linear data structure where elements are stored in nodes connected by pointers."
        },
        {
            "text": "What is the time complexity of inserting at the beginning of a linked list?",
            "option1": "O(1)",
            "option2": "O(n)",
            "option3": "O(log n)",
            "option4": "O(n²)",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "Inserting at the beginning of a linked list is O(1) as it only requires updating the head pointer."
        },
        {
            "text": "What is a binary tree?",
            "option1": "A tree with at most 2 children per node",
            "option2": "A tree with exactly 2 children",
            "option3": "A linear structure",
            "option4": "An array",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "A binary tree is a tree data structure where each node has at most two children."
        },
        {
            "text": "What is the height of a balanced binary tree with n nodes?",
            "option1": "O(1)",
            "option2": "O(n)",
            "option3": "O(log n)",
            "option4": "O(n²)",
            "correct_option": 3,
            "difficulty": "Hard",
            "explanation": "A balanced binary tree has height O(log n) where n is the number of nodes."
        },
        {
            "text": "What is hashing?",
            "option1": "A technique to map data to array indices",
            "option2": "Sorting algorithm",
            "option3": "Searching algorithm",
            "option4": "Tree traversal",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "Hashing is a technique that maps data to array indices using a hash function."
        },
        {
            "text": "What is the worst-case time complexity of quicksort?",
            "option1": "O(n log n)",
            "option2": "O(n)",
            "option3": "O(n²)",
            "option4": "O(log n)",
            "correct_option": 3,
            "difficulty": "Hard",
            "explanation": "Quicksort has worst-case time complexity O(n²) when the pivot is always the smallest or largest element."
        }
    ],
    "General Knowledge": [
        {
            "text": "What is the capital of France?",
            "option1": "London",
            "option2": "Berlin",
            "option3": "Paris",
            "option4": "Madrid",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "Paris is the capital and largest city of France."
        },
        {
            "text": "Which planet is known as the Red Planet?",
            "option1": "Venus",
            "option2": "Mars",
            "option3": "Jupiter",
            "option4": "Saturn",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Mars is called the Red Planet due to iron oxide on its surface."
        },
        {
            "text": "Who wrote 'Romeo and Juliet'?",
            "option1": "Charles Dickens",
            "option2": "William Shakespeare",
            "option3": "Jane Austen",
            "option4": "Mark Twain",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Romeo and Juliet is a tragedy written by William Shakespeare."
        },
        {
            "text": "What is the largest ocean on Earth?",
            "option1": "Atlantic Ocean",
            "option2": "Indian Ocean",
            "option3": "Arctic Ocean",
            "option4": "Pacific Ocean",
            "correct_option": 4,
            "difficulty": "Easy",
            "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth."
        },
        {
            "text": "In which year did World War II end?",
            "option1": "1943",
            "option2": "1944",
            "option3": "1945",
            "option4": "1946",
            "correct_option": 3,
            "difficulty": "Medium",
            "explanation": "World War II ended in 1945 with the surrender of Japan."
        },
        {
            "text": "What is the chemical symbol for gold?",
            "option1": "Go",
            "option2": "Gd",
            "option3": "Au",
            "option4": "Ag",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "Au is the chemical symbol for gold, derived from the Latin word 'aurum'."
        },
        {
            "text": "Who painted the Mona Lisa?",
            "option1": "Vincent van Gogh",
            "option2": "Pablo Picasso",
            "option3": "Leonardo da Vinci",
            "option4": "Michelangelo",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "The Mona Lisa was painted by Leonardo da Vinci in the 16th century."
        },
        {
            "text": "What is the smallest prime number?",
            "option1": "0",
            "option2": "1",
            "option3": "2",
            "option4": "3",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "2 is the smallest and only even prime number."
        },
        {
            "text": "Which gas makes up most of Earth's atmosphere?",
            "option1": "Oxygen",
            "option2": "Carbon Dioxide",
            "option3": "Nitrogen",
            "option4": "Argon",
            "correct_option": 3,
            "difficulty": "Medium",
            "explanation": "Nitrogen makes up approximately 78% of Earth's atmosphere."
        },
        {
            "text": "What is the speed of light in vacuum?",
            "option1": "300,000 km/s",
            "option2": "150,000 km/s",
            "option3": "450,000 km/s",
            "option4": "600,000 km/s",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "The speed of light in vacuum is approximately 299,792,458 m/s or about 300,000 km/s."
        }
    ],
    "Java Programming": [
        {
            "text": "What is Java?",
            "option1": "A programming language",
            "option2": "A coffee brand",
            "option3": "An operating system",
            "option4": "A database",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "Java is an object-oriented programming language developed by Sun Microsystems."
        },
        {
            "text": "What is JVM?",
            "option1": "Java Virtual Machine",
            "option2": "Java Variable Manager",
            "option3": "Java Version Manager",
            "option4": "Java Value Method",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "JVM (Java Virtual Machine) is a virtual machine that enables Java programs to run on any device."
        },
        {
            "text": "What is the main method signature in Java?",
            "option1": "public static void main(String args)",
            "option2": "public static void main(String[] args)",
            "option3": "private static void main(String[] args)",
            "option4": "public void main(String[] args)",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "The main method must be public, static, void, and take String[] as parameter."
        },
        {
            "text": "What is inheritance in Java?",
            "option1": "Creating objects",
            "option2": "A class acquiring properties of another class",
            "option3": "Memory management",
            "option4": "Exception handling",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "Inheritance allows a class to inherit properties and methods from a parent class."
        },
        {
            "text": "What is an interface in Java?",
            "option1": "A class",
            "option2": "A contract that defines methods",
            "option3": "A variable",
            "option4": "A package",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "An interface is a contract that defines a set of methods that implementing classes must provide."
        },
        {
            "text": "What is the difference between == and equals() in Java?",
            "option1": "== compares references, equals() compares values",
            "option2": "No difference",
            "option3": "== compares values, equals() compares references",
            "option4": "Both are same",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "== compares object references, while equals() compares the actual values/content."
        },
        {
            "text": "What is a constructor in Java?",
            "option1": "A method that destroys objects",
            "option2": "A special method that initializes objects",
            "option3": "A variable",
            "option4": "A class",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "A constructor is a special method used to initialize objects when they are created."
        },
        {
            "text": "What is polymorphism in Java?",
            "option1": "Having multiple forms",
            "option2": "Single form",
            "option3": "Memory allocation",
            "option4": "Variable declaration",
            "correct_option": 1,
            "difficulty": "Hard",
            "explanation": "Polymorphism allows objects of different types to be accessed through the same interface."
        },
        {
            "text": "What is the super keyword in Java?",
            "option1": "Refers to parent class",
            "option2": "Refers to current class",
            "option3": "Refers to child class",
            "option4": "A variable",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "The super keyword refers to the parent class and is used to call parent class methods and constructors."
        },
        {
            "text": "What is exception handling in Java?",
            "option1": "Managing runtime errors",
            "option2": "Creating errors",
            "option3": "Ignoring errors",
            "option4": "Preventing compilation",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "Exception handling allows programs to handle runtime errors gracefully using try-catch blocks."
        }
    ],
    "Logical Reasoning": [
        {
            "text": "If all roses are flowers and some flowers are red, then:",
            "option1": "All roses are red",
            "option2": "Some roses are red",
            "option3": "No roses are red",
            "option4": "Cannot be determined",
            "correct_option": 4,
            "difficulty": "Medium",
            "explanation": "We cannot determine if roses are red based on the given information."
        },
        {
            "text": "Complete the series: 2, 4, 8, 16, ?",
            "option1": "24",
            "option2": "32",
            "option3": "28",
            "option4": "20",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Each number is multiplied by 2: 2×2=4, 4×2=8, 8×2=16, 16×2=32."
        },
        {
            "text": "If Monday is the first day, what is the 100th day?",
            "option1": "Monday",
            "option2": "Tuesday",
            "option3": "Wednesday",
            "option4": "Thursday",
            "correct_option": 2,
            "difficulty": "Hard",
            "explanation": "100 mod 7 = 2, so it's 2 days after Monday, which is Tuesday."
        },
        {
            "text": "A is taller than B, B is taller than C. Who is tallest?",
            "option1": "A",
            "option2": "B",
            "option3": "C",
            "option4": "Cannot determine",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A > B > C, so A is the tallest."
        },
        {
            "text": "If all cats are animals and some animals are pets, then:",
            "option1": "All cats are pets",
            "option2": "Some cats are pets",
            "option3": "No cats are pets",
            "option4": "Cannot be determined",
            "correct_option": 4,
            "difficulty": "Medium",
            "explanation": "We cannot determine if cats are pets from the given information."
        },
        {
            "text": "Find the odd one out: Apple, Banana, Carrot, Orange",
            "option1": "Apple",
            "option2": "Banana",
            "option3": "Carrot",
            "option4": "Orange",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "Carrot is a vegetable, while others are fruits."
        },
        {
            "text": "Complete: Dog is to Puppy as Cat is to ?",
            "option1": "Kitten",
            "option2": "Cub",
            "option3": "Calf",
            "option4": "Chick",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A young dog is a puppy, similarly a young cat is a kitten."
        },
        {
            "text": "If 5 workers can build a wall in 10 days, how many days for 10 workers?",
            "option1": "5 days",
            "option2": "10 days",
            "option3": "15 days",
            "option4": "20 days",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "More workers means less time. 5 workers × 10 days = 10 workers × 5 days."
        },
        {
            "text": "What comes next: Z, Y, X, W, ?",
            "option1": "V",
            "option2": "U",
            "option3": "T",
            "option4": "S",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "The series is going backwards in the alphabet: Z, Y, X, W, V."
        },
        {
            "text": "If RED is coded as 1854, how is BLUE coded?",
            "option1": "212215",
            "option2": "221215",
            "option3": "212125",
            "option4": "221225",
            "correct_option": 2,
            "difficulty": "Hard",
            "explanation": "R=18, E=5, D=4. Similarly B=2, L=12, U=21, E=5, so BLUE = 221215."
        }
    ],
    "Python Programming": [
        {
            "text": "What is Python?",
            "option1": "A snake",
            "option2": "A programming language",
            "option3": "An operating system",
            "option4": "A database",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Python is a high-level, interpreted programming language."
        },
        {
            "text": "What is the correct way to create a list in Python?",
            "option1": "list = (1, 2, 3)",
            "option2": "list = [1, 2, 3]",
            "option3": "list = {1, 2, 3}",
            "option4": "list = <1, 2, 3>",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Lists in Python are created using square brackets []."
        },
        {
            "text": "What is a dictionary in Python?",
            "option1": "A list of words",
            "option2": "A key-value pair data structure",
            "option3": "A function",
            "option4": "A variable",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "A dictionary stores data in key-value pairs using curly braces {}."
        },
        {
            "text": "What does len() function do in Python?",
            "option1": "Returns the length of a string or list",
            "option2": "Converts to integer",
            "option3": "Prints output",
            "option4": "Deletes items",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "len() returns the number of items in a sequence or collection."
        },
        {
            "text": "What is list comprehension in Python?",
            "option1": "A way to create lists concisely",
            "option2": "A function",
            "option3": "A variable",
            "option4": "A loop",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "List comprehension provides a concise way to create lists based on existing lists."
        },
        {
            "text": "What is the difference between == and is in Python?",
            "option1": "== compares values, is compares identity",
            "option2": "No difference",
            "option3": "== compares identity, is compares values",
            "option4": "Both are same",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "== compares the values, while 'is' compares if two variables point to the same object."
        },
        {
            "text": "What is a tuple in Python?",
            "option1": "An immutable list",
            "option2": "A mutable list",
            "option3": "A function",
            "option4": "A variable",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A tuple is an immutable (unchangeable) ordered sequence of elements."
        },
        {
            "text": "What does the range() function return?",
            "option1": "A list",
            "option2": "A range object",
            "option3": "A tuple",
            "option4": "A dictionary",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "range() returns a range object that represents a sequence of numbers."
        },
        {
            "text": "What is a lambda function in Python?",
            "option1": "An anonymous function",
            "option2": "A named function",
            "option3": "A class",
            "option4": "A module",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "A lambda function is a small anonymous function defined with the lambda keyword."
        },
        {
            "text": "What is the purpose of __init__ in Python?",
            "option1": "To initialize an object",
            "option2": "To delete an object",
            "option3": "To print output",
            "option4": "To import modules",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "__init__ is a special method called when an object is instantiated to initialize it."
        }
    ],
    "Quantitative Aptitude": [
        {
            "text": "What is 15% of 200?",
            "option1": "20",
            "option2": "30",
            "option3": "40",
            "option4": "50",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "15% of 200 = (15/100) × 200 = 30"
        },
        {
            "text": "If x + 5 = 12, what is x?",
            "option1": "5",
            "option2": "6",
            "option3": "7",
            "option4": "8",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "x + 5 = 12, so x = 12 - 5 = 7"
        },
        {
            "text": "What is the square root of 144?",
            "option1": "10",
            "option2": "11",
            "option3": "12",
            "option4": "13",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "12 × 12 = 144, so √144 = 12"
        },
        {
            "text": "If a train travels 120 km in 2 hours, what is its speed?",
            "option1": "50 km/h",
            "option2": "60 km/h",
            "option3": "70 km/h",
            "option4": "80 km/h",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Speed = Distance/Time = 120/2 = 60 km/h"
        },
        {
            "text": "What is the area of a rectangle with length 8 and width 5?",
            "option1": "35",
            "option2": "40",
            "option3": "45",
            "option4": "50",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Area = length × width = 8 × 5 = 40"
        },
        {
            "text": "What is 2³?",
            "option1": "4",
            "option2": "6",
            "option3": "8",
            "option4": "10",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "2³ = 2 × 2 × 2 = 8"
        },
        {
            "text": "If 3x = 21, what is x?",
            "option1": "5",
            "option2": "6",
            "option3": "7",
            "option4": "8",
            "correct_option": 3,
            "difficulty": "Easy",
            "explanation": "3x = 21, so x = 21/3 = 7"
        },
        {
            "text": "What is the average of 10, 20, 30?",
            "option1": "15",
            "option2": "20",
            "option3": "25",
            "option4": "30",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Average = (10 + 20 + 30)/3 = 60/3 = 20"
        },
        {
            "text": "What is the perimeter of a square with side 6?",
            "option1": "20",
            "option2": "24",
            "option3": "28",
            "option4": "30",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "Perimeter of square = 4 × side = 4 × 6 = 24"
        },
        {
            "text": "If 25% of a number is 50, what is the number?",
            "option1": "150",
            "option2": "200",
            "option3": "250",
            "option4": "300",
            "correct_option": 2,
            "difficulty": "Medium",
            "explanation": "25% of x = 50, so (25/100) × x = 50, therefore x = 50 × 4 = 200"
        }
    ],
    "SQL": [
        {
            "text": "What does SQL stand for?",
            "option1": "Structured Query Language",
            "option2": "Simple Query Language",
            "option3": "Standard Query Language",
            "option4": "System Query Language",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "SQL stands for Structured Query Language."
        },
        {
            "text": "Which SQL command is used to retrieve data?",
            "option1": "INSERT",
            "option2": "SELECT",
            "option3": "UPDATE",
            "option4": "DELETE",
            "correct_option": 2,
            "difficulty": "Easy",
            "explanation": "SELECT is used to retrieve data from a database."
        },
        {
            "text": "What is a primary key?",
            "option1": "A unique identifier for a row",
            "option2": "A foreign key",
            "option3": "A column name",
            "option4": "A table name",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "A primary key is a unique identifier that uniquely identifies each row in a table."
        },
        {
            "text": "What does WHERE clause do in SQL?",
            "option1": "Filters rows",
            "option2": "Groups rows",
            "option3": "Orders rows",
            "option4": "Joins tables",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "WHERE clause is used to filter records based on specified conditions."
        },
        {
            "text": "What is the difference between DELETE and DROP?",
            "option1": "DELETE removes rows, DROP removes table",
            "option2": "No difference",
            "option3": "DELETE removes table, DROP removes rows",
            "option4": "Both are same",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "DELETE removes rows from a table, while DROP removes the entire table structure."
        },
        {
            "text": "What does JOIN do in SQL?",
            "option1": "Combines rows from multiple tables",
            "option2": "Deletes tables",
            "option3": "Creates tables",
            "option4": "Updates tables",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "JOIN combines rows from two or more tables based on a related column."
        },
        {
            "text": "What is a foreign key?",
            "option1": "A key that references another table's primary key",
            "option2": "A primary key",
            "option3": "A unique key",
            "option4": "A column name",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "A foreign key is a column that references the primary key of another table."
        },
        {
            "text": "What does GROUP BY do?",
            "option1": "Groups rows with same values",
            "option2": "Orders rows",
            "option3": "Filters rows",
            "option4": "Joins tables",
            "correct_option": 1,
            "difficulty": "Medium",
            "explanation": "GROUP BY groups rows that have the same values in specified columns."
        },
        {
            "text": "What is the purpose of ORDER BY?",
            "option1": "To sort results",
            "option2": "To filter results",
            "option3": "To group results",
            "option4": "To join tables",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "ORDER BY is used to sort the result set in ascending or descending order."
        },
        {
            "text": "What does COUNT() function do?",
            "option1": "Counts the number of rows",
            "option2": "Counts columns",
            "option3": "Counts tables",
            "option4": "Counts databases",
            "correct_option": 1,
            "difficulty": "Easy",
            "explanation": "COUNT() returns the number of rows that match a specified condition."
        }
    ]
}

with app.app_context():
    print("Adding sample questions to database...")
    
    for category_name, questions in questions_data.items():
        # Get or create category
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            print(f"Category '{category_name}' not found. Creating it...")
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
        
        # Add questions for this category
        added = 0
        for q_data in questions:
            # Check if question already exists
            existing = Question.query.filter_by(text=q_data['text']).first()
            if not existing:
                question = Question(
                    text=q_data['text'],
                    option1=q_data['option1'],
                    option2=q_data['option2'],
                    option3=q_data.get('option3', ''),
                    option4=q_data.get('option4', ''),
                    correct_option=q_data['correct_option'],
                    difficulty=q_data.get('difficulty', 'Medium'),
                    explanation=q_data.get('explanation', ''),
                    category_id=category.id
                )
                db.session.add(question)
                added += 1
        
        db.session.commit()
        print(f"Added {added} questions for '{category_name}' category")
    
    print("\nAll questions added successfully!")
    print(f"Total categories: {Category.query.count()}")
    print(f"Total questions: {Question.query.count()}")

