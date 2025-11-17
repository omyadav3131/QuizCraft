"""
HEADER_COMMENT_AUTOGEN
FILE: add_all_questions.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

#!/usr/bin/env python
# add_all_questions.py - Add 10-10 questions for each difficulty level in all categories

from app import create_app, db
from app.models import Question, Category

app = create_app()

# Comprehensive questions for all categories and difficulty levels
all_questions = {
    "Quantitative Aptitude": {
        "Easy": [
            {"text": "What is 25% of 400?", "option1": "50", "option2": "75", "option3": "100", "option4": "125", "correct_option": 3},
            {"text": "If 2x = 16, what is x?", "option1": "6", "option2": "7", "option3": "8", "option4": "9", "correct_option": 3},
            {"text": "What is the square of 7?", "option1": "42", "option2": "49", "option3": "56", "option4": "63", "correct_option": 2},
            {"text": "What is 50% of 200?", "option1": "75", "option2": "100", "option3": "125", "option4": "150", "correct_option": 2},
            {"text": "If a book costs 300 and has 20% discount, what is the final price?", "option1": "210", "option2": "220", "option3": "230", "option4": "240", "correct_option": 4},
            {"text": "What is 10% of 500?", "option1": "40", "option2": "50", "option3": "60", "option4": "70", "correct_option": 2},
            {"text": "What is the area of a circle with radius 5?", "option1": "25π", "option2": "50π", "option3": "75π", "option4": "100π", "correct_option": 1},
            {"text": "What is 3 + 3 * 2?", "option1": "9", "option2": "12", "option3": "15", "option4": "18", "correct_option": 1},
            {"text": "What is 20% of 150?", "option1": "25", "option2": "30", "option3": "35", "option4": "40", "correct_option": 2},
            {"text": "If 5y = 25, what is y?", "option1": "3", "option2": "4", "option3": "5", "option4": "6", "correct_option": 3},
        ],
        "Medium": [
            {"text": "If x + 5 = 12, what is x?", "option1": "5", "option2": "6", "option3": "7", "option4": "8", "correct_option": 3},
            {"text": "What is 15% of 300?", "option1": "40", "option2": "45", "option3": "50", "option4": "55", "correct_option": 2},
            {"text": "A train travels 120 km in 2 hours. What is its speed?", "option1": "50 km/h", "option2": "60 km/h", "option3": "70 km/h", "option4": "80 km/h", "correct_option": 2},
            {"text": "What is the perimeter of a rectangle with length 8 and width 5?", "option1": "26", "option2": "40", "option3": "45", "option4": "50", "correct_option": 1},
            {"text": "If the ratio is 2:3 and total is 50, what is the first part?", "option1": "15", "option2": "20", "option3": "25", "option4": "30", "correct_option": 2},
            {"text": "What is 2^5?", "option1": "16", "option2": "25", "option3": "32", "option4": "64", "correct_option": 3},
            {"text": "What is the average of 10, 20, 30, 40?", "option1": "20", "option2": "25", "option3": "30", "option4": "35", "correct_option": 2},
            {"text": "If a number is 40% of 200, what is the number?", "option1": "60", "option2": "70", "option3": "80", "option4": "90", "correct_option": 3},
            {"text": "What is √36?", "option1": "4", "option2": "5", "option3": "6", "option4": "7", "correct_option": 3},
            {"text": "What is 3/4 of 120?", "option1": "80", "option2": "90", "option3": "100", "option4": "110", "correct_option": 2},
        ],
        "Hard": [
            {"text": "If x + y = 10 and x - y = 2, what is x?", "option1": "4", "option2": "6", "option3": "8", "option4": "12", "correct_option": 2},
            {"text": "A person invests 1000 at 10% per annum for 2 years. What is the simple interest?", "option1": "100", "option2": "150", "option3": "200", "option4": "250", "correct_option": 3},
            {"text": "What is the LCM of 12 and 18?", "option1": "24", "option2": "30", "option3": "36", "option4": "42", "correct_option": 3},
            {"text": "If 30% of a number is 60, what is the number?", "option1": "100", "option2": "150", "option3": "200", "option4": "250", "correct_option": 3},
            {"text": "What is the GCD of 24 and 36?", "option1": "6", "option2": "8", "option3": "12", "option4": "18", "correct_option": 3},
            {"text": "If a:b = 3:4 and b:c = 4:5, what is a:c?", "option1": "3:5", "option2": "3:4", "option3": "4:5", "option4": "5:6", "correct_option": 1},
            {"text": "What is 15% of 15% of 400?", "option1": "5", "option2": "7", "option3": "9", "option4": "11", "correct_option": 3},
            {"text": "If x^2 = 144, what is x?", "option1": "10", "option2": "11", "option3": "12", "option4": "13", "correct_option": 3},
            {"text": "A number when divided by 5 gives remainder 3. The number could be?", "option1": "13", "option2": "14", "option3": "15", "option4": "16", "correct_option": 1},
            {"text": "What is 2^3 + 3^2?", "option1": "15", "option2": "17", "option3": "19", "option4": "21", "correct_option": 2},
        ]
    },
    "Logical Reasoning": {
        "Easy": [
            {"text": "If A > B and B > C, who is smallest?", "option1": "A", "option2": "B", "option3": "C", "option4": "Cannot determine", "correct_option": 3},
            {"text": "Find the odd one: Cat, Dog, Fish, Chair", "option1": "Cat", "option2": "Dog", "option3": "Fish", "option4": "Chair", "correct_option": 4},
            {"text": "What comes next: 1, 2, 4, 8, ?", "option1": "10", "option2": "12", "option3": "16", "option4": "20", "correct_option": 3},
            {"text": "Complete: Hand is to Glove as Foot is to ?", "option1": "Shoe", "option2": "Sock", "option3": "Boot", "option4": "Sandal", "correct_option": 1},
            {"text": "What comes next: Z, Y, X, W, ?", "option1": "U", "option2": "V", "option3": "T", "option4": "S", "correct_option": 1},
            {"text": "If all dogs are animals and all animals have legs, then dogs have legs - True or False?", "option1": "True", "option2": "False", "option3": "Cannot determine", "option4": "Insufficient data", "correct_option": 1},
            {"text": "What comes next: 2, 4, 6, 8, ?", "option1": "9", "option2": "10", "option3": "11", "option4": "12", "correct_option": 2},
            {"text": "Find the odd one: Red, Blue, Green, Tall", "option1": "Red", "option2": "Blue", "option3": "Green", "option4": "Tall", "correct_option": 4},
            {"text": "If E = 5, then Z = ?", "option1": "24", "option2": "25", "option3": "26", "option4": "27", "correct_option": 3},
            {"text": "What comes next: A, C, E, G, ?", "option1": "H", "option2": "I", "option3": "J", "option4": "K", "correct_option": 2},
        ],
        "Medium": [
            {"text": "If Monday is the first day, what is the 100th day?", "option1": "Monday", "option2": "Tuesday", "option3": "Wednesday", "option4": "Thursday", "correct_option": 2},
            {"text": "Complete the series: 5, 10, 20, 40, ?", "option1": "50", "option2": "60", "option3": "80", "option4": "100", "correct_option": 3},
            {"text": "What comes next: 1, 1, 2, 3, 5, 8, ?", "option1": "10", "option2": "11", "option3": "12", "option4": "13", "correct_option": 4},
            {"text": "If all cats are animals and some animals are pets, then?", "option1": "All cats are pets", "option2": "Some cats are pets", "option3": "No cats are pets", "option4": "Cannot determine", "correct_option": 4},
            {"text": "What comes next: 3, 6, 9, 12, ?", "option1": "13", "option2": "14", "option3": "15", "option4": "16", "correct_option": 3},
            {"text": "Find the odd one: 10, 20, 30, 35", "option1": "10", "option2": "20", "option3": "30", "option4": "35", "correct_option": 4},
            {"text": "If 5 workers build a wall in 10 days, how many days for 10 workers?", "option1": "5 days", "option2": "10 days", "option3": "15 days", "option4": "20 days", "correct_option": 1},
            {"text": "What comes next: 1, 4, 9, 16, ?", "option1": "20", "option2": "24", "option3": "25", "option4": "30", "correct_option": 3},
            {"text": "Complete the series: 2, 6, 12, 20, ?", "option1": "28", "option2": "30", "option3": "32", "option4": "36", "correct_option": 2},
            {"text": "If RED = 27, then BLUE = ?", "option1": "40", "option2": "45", "option3": "50", "option4": "55", "correct_option": 2},
        ],
        "Hard": [
            {"text": "What comes next: 1, 8, 27, 64, ?", "option1": "100", "option2": "125", "option3": "144", "option4": "169", "correct_option": 2},
            {"text": "If all A are B, all B are C, then?", "option1": "All A are C", "option2": "All C are A", "option3": "Some A are C", "option4": "No A are C", "correct_option": 1},
            {"text": "Complete: 2, 3, 5, 7, 11, ?", "option1": "12", "option2": "13", "option3": "14", "option4": "15", "correct_option": 2},
            {"text": "What comes next: 1, 2, 4, 7, 11, ?", "option1": "15", "option2": "16", "option3": "17", "option4": "18", "correct_option": 2},
            {"text": "If ABCD = 10, BCDE = 14, then CDEF = ?", "option1": "18", "option2": "19", "option3": "20", "option4": "21", "correct_option": 2},
            {"text": "Find the missing number: 6, 11, ?, 27, 38", "option1": "16", "option2": "17", "option3": "18", "option4": "19", "correct_option": 3},
            {"text": "What comes next: 10, 11, 13, 16, 20, ?", "option1": "24", "option2": "25", "option3": "26", "option4": "27", "correct_option": 2},
            {"text": "If + = *, - = +, * = -, then 10 - 5 + 2 = ?", "option1": "7", "option2": "8", "option3": "15", "option4": "17", "correct_option": 3},
            {"text": "Find the pattern: 121, 144, 169, ?", "option1": "196", "option2": "200", "option3": "225", "option4": "256", "correct_option": 1},
            {"text": "What comes next: 2, 5, 10, 17, 26, ?", "option1": "35", "option2": "36", "option3": "37", "option4": "38", "correct_option": 3},
        ]
    },
    "General Knowledge": {
        "Easy": [
            {"text": "What is the largest country by area?", "option1": "China", "option2": "USA", "option3": "Russia", "option4": "Canada", "correct_option": 3},
            {"text": "Which is the longest river in the world?", "option1": "Amazon", "option2": "Nile", "option3": "Yangtze", "option4": "Mississippi", "correct_option": 2},
            {"text": "What is the currency of Japan?", "option1": "Yuan", "option2": "Won", "option3": "Yen", "option4": "Ringgit", "correct_option": 3},
            {"text": "Who wrote the Indian National Anthem?", "option1": "Rabindranath Tagore", "option2": "Bankim Chandra", "option3": "Keshab Chandra Sen", "option4": "Ram Mohan Roy", "correct_option": 1},
            {"text": "In which year did India gain independence?", "option1": "1945", "option2": "1947", "option3": "1950", "option4": "1952", "correct_option": 2},
            {"text": "What is the national animal of India?", "option1": "Lion", "option2": "Tiger", "option3": "Elephant", "option4": "Peacock", "correct_option": 2},
            {"text": "What is the capital of France?", "option1": "London", "option2": "Berlin", "option3": "Paris", "option4": "Madrid", "correct_option": 3},
            {"text": "Which planet is known as the Red Planet?", "option1": "Venus", "option2": "Mars", "option3": "Jupiter", "option4": "Saturn", "correct_option": 2},
            {"text": "Who wrote Romeo and Juliet?", "option1": "Charles Dickens", "option2": "William Shakespeare", "option3": "Jane Austen", "option4": "Mark Twain", "correct_option": 2},
            {"text": "What is the largest ocean?", "option1": "Atlantic", "option2": "Indian", "option3": "Arctic", "option4": "Pacific", "correct_option": 4},
        ],
        "Medium": [
            {"text": "In which year did World War II end?", "option1": "1943", "option2": "1944", "option3": "1945", "option4": "1946", "correct_option": 3},
            {"text": "What is the chemical symbol for gold?", "option1": "Go", "option2": "Gd", "option3": "Au", "option4": "Ag", "correct_option": 3},
            {"text": "Who painted the Mona Lisa?", "option1": "Van Gogh", "option2": "Picasso", "option3": "Leonardo da Vinci", "option4": "Michelangelo", "correct_option": 3},
            {"text": "What is the smallest prime number?", "option1": "0", "option2": "1", "option3": "2", "option4": "3", "correct_option": 3},
            {"text": "Which gas makes up most of Earth's atmosphere?", "option1": "Oxygen", "option2": "Carbon Dioxide", "option3": "Nitrogen", "option4": "Argon", "correct_option": 3},
            {"text": "What is the speed of light in vacuum?", "option1": "300,000 km/s", "option2": "150,000 km/s", "option3": "450,000 km/s", "option4": "600,000 km/s", "correct_option": 1},
            {"text": "Who invented the telephone?", "option1": "Thomas Edison", "option2": "Alexander Graham Bell", "option3": "Nikola Tesla", "option4": "George Washington", "correct_option": 2},
            {"text": "What is the capital of Australia?", "option1": "Sydney", "option2": "Melbourne", "option3": "Canberra", "option4": "Brisbane", "correct_option": 3},
            {"text": "Which country has the most population?", "option1": "India", "option2": "USA", "option3": "Indonesia", "option4": "China", "correct_option": 1},
            {"text": "What is the largest mammal?", "option1": "Elephant", "option2": "Giraffe", "option3": "Blue Whale", "option4": "Hippopotamus", "correct_option": 3},
        ],
        "Hard": [
            {"text": "In which year was the United Nations founded?", "option1": "1942", "option2": "1943", "option3": "1945", "option4": "1947", "correct_option": 3},
            {"text": "Who was the first President of India?", "option1": "Jawaharlal Nehru", "option2": "Dr. Rajendra Prasad", "option3": "Sardar Vallabhbhai Patel", "option4": "Lal Bahadur Shastri", "correct_option": 2},
            {"text": "What is the Magna Carta?", "option1": "A document limiting royal power", "option2": "A ship", "option3": "A battle", "option4": "A book", "correct_option": 1},
            {"text": "Who discovered the theory of relativity?", "option1": "Newton", "option2": "Einstein", "option3": "Planck", "option4": "Bohr", "correct_option": 2},
            {"text": "What is the smallest country in the world by area?", "option1": "Monaco", "option2": "Vatican City", "option3": "San Marino", "option4": "Liechtenstein", "correct_option": 2},
            {"text": "Which empire built the Great Wall of China?", "option1": "Han", "option2": "Ming", "option3": "Tang", "option4": "Song", "correct_option": 2},
            {"text": "What is the Renaissance?", "option1": "A war", "option2": "A cultural movement", "option3": "A treaty", "option4": "A revolution", "correct_option": 2},
            {"text": "Who wrote Das Kapital?", "option1": "Vladimir Lenin", "option2": "Leon Trotsky", "option3": "Karl Marx", "option4": "Friedrich Engels", "correct_option": 3},
            {"text": "What is the primary language of Brazil?", "option1": "Spanish", "option2": "Portuguese", "option3": "Brazilian", "option4": "Brasilian", "correct_option": 2},
            {"text": "Which desert is the largest in the world?", "option1": "Sahara", "option2": "Gobi", "option3": "Kalahari", "option4": "Arabian", "correct_option": 1},
        ]
    },
    "Java Programming": {
        "Easy": [
            {"text": "What does JDK stand for?", "option1": "Java Development Kit", "option2": "Java Debug Kit", "option3": "Java Design Kit", "option4": "Java Deployment Kit", "correct_option": 1},
            {"text": "Which keyword is used to inherit a class in Java?", "option1": "inherit", "option2": "extends", "option3": "implements", "option4": "extends or implements", "correct_option": 2},
            {"text": "What is the default value of boolean in Java?", "option1": "true", "option2": "false", "option3": "null", "option4": "0", "correct_option": 2},
            {"text": "Which package is always imported in Java?", "option1": "java.lang", "option2": "java.util", "option3": "java.io", "option4": "java.net", "correct_option": 1},
            {"text": "What is the size of byte in Java?", "option1": "1 bit", "option2": "1 byte", "option3": "2 bytes", "option4": "4 bytes", "correct_option": 2},
            {"text": "Which method is the entry point of a Java program?", "option1": "run()", "option2": "start()", "option3": "main()", "option4": "init()", "correct_option": 3},
            {"text": "What is a class in Java?", "option1": "A function", "option2": "Blueprint for objects", "option3": "A variable", "option4": "A library", "correct_option": 2},
            {"text": "What does JVM stand for?", "option1": "Java Virtual Machine", "option2": "Java Variable Manager", "option3": "Java Version Manager", "option4": "Java Value Method", "correct_option": 1},
            {"text": "What keyword is used to prevent method overriding?", "option1": "private", "option2": "static", "option3": "final", "option4": "protected", "correct_option": 3},
            {"text": "What is an interface in Java?", "option1": "A class", "option2": "A contract defining methods", "option3": "A variable", "option4": "A package", "correct_option": 2},
        ],
        "Medium": [
            {"text": "What is the difference between == and equals() in Java?", "option1": "== compares references, equals() compares values", "option2": "No difference", "option3": "== compares values, equals() compares references", "option4": "Both are same", "correct_option": 1},
            {"text": "What is the difference between ArrayList and LinkedList?", "option1": "ArrayList is faster for random access", "option2": "LinkedList is faster for random access", "option3": "No difference", "option4": "ArrayList uses less memory", "correct_option": 1},
            {"text": "What is a constructor in Java?", "option1": "Destroys objects", "option2": "Initializes objects", "option3": "A variable", "option4": "A function", "correct_option": 2},
            {"text": "What is the purpose of the abstract keyword?", "option1": "To hide implementation", "option2": "To prevent instantiation", "option3": "To optimize code", "option4": "To encrypt data", "correct_option": 2},
            {"text": "What is the difference between static and non-static methods?", "option1": "Static methods can access instance variables", "option2": "Non-static methods don't need an object", "option3": "Static methods belong to class, not object", "option4": "No difference", "correct_option": 3},
            {"text": "What is exception handling in Java?", "option1": "Preventing errors", "option2": "Handling runtime errors gracefully", "option3": "Creating errors", "option4": "Ignoring errors", "correct_option": 2},
            {"text": "What is the purpose of finally block?", "option1": "To catch exceptions", "option2": "To execute code regardless of exception", "option3": "To throw exceptions", "option4": "To create finally statements", "correct_option": 2},
            {"text": "What is method overloading?", "option1": "Having multiple methods with same name but different parameters", "option2": "Having methods with different names", "option3": "Having multiple classes", "option4": "Having multiple objects", "correct_option": 1},
            {"text": "What is method overriding?", "option1": "Redefining parent class method in child class", "option2": "Creating new methods", "option3": "Deleting methods", "option4": "Calling methods multiple times", "correct_option": 1},
            {"text": "What is the super keyword used for?", "option1": "Refers to parent class", "option2": "Refers to current class", "option3": "Refers to child class", "option4": "A variable", "correct_option": 1},
        ],
        "Hard": [
            {"text": "What is polymorphism in Java?", "option1": "Having multiple forms", "option2": "Single form", "option3": "Memory allocation", "option4": "Variable declaration", "correct_option": 1},
            {"text": "What is encapsulation?", "option1": "Hiding data and methods within a class", "option2": "Inheriting from multiple classes", "option3": "Using pointers", "option4": "Memory management", "correct_option": 1},
            {"text": "What is the difference between shallow copy and deep copy?", "option1": "Shallow copy copies object reference, deep copy copies data", "option2": "No difference", "option3": "Shallow copy is faster", "option4": "Deep copy uses less memory", "correct_option": 1},
            {"text": "What is garbage collection in Java?", "option1": "Collecting garbage from code", "option2": "Automatic memory management", "option3": "Removing unnecessary code", "option4": "Cleaning variables", "correct_option": 2},
            {"text": "What is the purpose of synchronized keyword?", "option1": "To synchronize clocks", "option2": "To make methods thread-safe", "option3": "To optimize code", "option4": "To prevent errors", "correct_option": 2},
            {"text": "What is a thread in Java?", "option1": "A lightweight process", "option2": "A heavy process", "option3": "A variable", "option4": "A method", "correct_option": 1},
            {"text": "What is the difference between Runnable and Thread?", "option1": "Runnable is an interface, Thread is a class", "option2": "Thread is faster", "option3": "Runnable uses more memory", "option4": "No difference", "correct_option": 1},
            {"text": "What is reflection in Java?", "option1": "Looking at objects in mirror", "option2": "Inspecting class structure at runtime", "option3": "Creating reflections", "option4": "A design pattern", "correct_option": 2},
            {"text": "What is serialization?", "option1": "Converting object to byte stream", "option2": "Creating series of objects", "option3": "Serial number assignment", "option4": "Object creation", "correct_option": 1},
            {"text": "What is the purpose of transient keyword?", "option1": "To prevent serialization of a field", "option2": "To speed up code", "option3": "To hide data", "option4": "To optimize memory", "correct_option": 1},
        ]
    },
    "Python Programming": {
        "Easy": [
            {"text": "Which symbol is used for comments in Python?", "option1": "//", "option2": "#", "option3": "--", "option4": "/*", "correct_option": 2},
            {"text": "What does PEP 8 relate to?", "option1": "Python version", "option2": "Coding style guide", "option3": "Python library", "option4": "Python compiler", "correct_option": 2},
            {"text": "Which function returns the type of an object in Python?", "option1": "typeof()", "option2": "type()", "option3": "gettype()", "option4": "classof()", "correct_option": 2},
            {"text": "What is the correct way to create a set in Python?", "option1": "set = (1, 2, 3)", "option2": "set = [1, 2, 3]", "option3": "set = {1, 2, 3}", "option4": "set = <1, 2, 3>", "correct_option": 3},
            {"text": "Which keyword is used to create a function in Python?", "option1": "function", "option2": "def", "option3": "func", "option4": "define", "correct_option": 2},
            {"text": "What is the output of print(2 ** 3)?", "option1": "5", "option2": "6", "option3": "8", "option4": "9", "correct_option": 3},
            {"text": "What is the correct way to create a list in Python?", "option1": "list = (1, 2, 3)", "option2": "list = [1, 2, 3]", "option3": "list = {1, 2, 3}", "option4": "list = <1, 2, 3>", "correct_option": 2},
            {"text": "What is a dictionary in Python?", "option1": "A list of words", "option2": "A key-value pair data structure", "option3": "A function", "option4": "A variable", "correct_option": 2},
            {"text": "What does len() function do?", "option1": "Returns length of string or list", "option2": "Converts to integer", "option3": "Prints output", "option4": "Deletes items", "correct_option": 1},
            {"text": "What is a tuple in Python?", "option1": "An immutable list", "option2": "A mutable list", "option3": "A function", "option4": "A variable", "correct_option": 1},
        ],
        "Medium": [
            {"text": "What is list comprehension?", "option1": "Understanding lists", "option2": "Creating lists concisely", "option3": "Compressing lists", "option4": "Sorting lists", "correct_option": 2},
            {"text": "What is the difference between == and is?", "option1": "== compares values, is compares identity", "option2": "No difference", "option3": "== compares identity, is compares values", "option4": "Both are same", "correct_option": 1},
            {"text": "What does the range() function return?", "option1": "A list", "option2": "A range object", "option3": "A tuple", "option4": "A dictionary", "correct_option": 2},
            {"text": "What is a lambda function?", "option1": "A named function", "option2": "An anonymous function", "option3": "A class", "option4": "A module", "correct_option": 2},
            {"text": "What is the purpose of __init__?", "option1": "Initializes an object", "option2": "Deletes an object", "option3": "Prints output", "option4": "Imports modules", "correct_option": 1},
            {"text": "What is the difference between append() and extend()?", "option1": "Both do the same thing", "option2": "append adds element, extend adds iterable", "option3": "extend is faster", "option4": "append adds multiple elements", "correct_option": 2},
            {"text": "What is the output of: x = [1,2,3]; print(x[:-1])?", "option1": "[1,2,3]", "option2": "[1,2]", "option3": "[2,3]", "option4": "[3]", "correct_option": 2},
            {"text": "What is slicing in Python?", "option1": "Cutting strings", "option2": "Extracting portion of sequence", "option3": "Dividing numbers", "option4": "Creating new lists", "correct_option": 2},
            {"text": "What is the difference between .split() and .join()?", "option1": "They do opposite operations", "option2": "No difference", "option3": "split is for lists", "option4": "join is for lists", "correct_option": 1},
            {"text": "What is *args in Python?", "option1": "A variable", "option2": "Variable number of arguments", "option3": "A function", "option4": "A module", "correct_option": 2},
        ],
        "Hard": [
            {"text": "What is a decorator in Python?", "option1": "A design pattern", "option2": "Function that modifies another function", "option3": "A class", "option4": "A variable", "correct_option": 2},
            {"text": "What is a generator in Python?", "option1": "Creates objects", "option2": "Generates numbers", "option3": "Yields values one at a time", "option4": "Generates code", "correct_option": 3},
            {"text": "What is the difference between __str__ and __repr__?", "option1": "No difference", "option2": "__str__ is for users, __repr__ for developers", "option3": "Both are same", "option4": "__repr__ is for users", "correct_option": 2},
            {"text": "What is metaclass in Python?", "option1": "A class for classes", "option2": "A super class", "option3": "A base class", "option4": "An abstract class", "correct_option": 1},
            {"text": "What is context manager in Python?", "option1": "Manages variables", "option2": "Manages resources using with statement", "option3": "Manages context", "option4": "Manages memory", "correct_option": 2},
            {"text": "What is the GIL in Python?", "option1": "A library", "option2": "Global Interpreter Lock", "option3": "A module", "option4": "A function", "correct_option": 2},
            {"text": "What is duck typing?", "option1": "A design pattern", "option2": "If it walks and quacks like a duck, it is a duck", "option3": "Type checking", "option4": "Variable naming", "correct_option": 2},
            {"text": "What is the difference between mutable and immutable?", "option1": "Mutable can be changed, immutable cannot", "option2": "No difference", "option3": "Immutable is faster", "option4": "Mutable uses more memory", "correct_option": 1},
            {"text": "What is monkey patching?", "option1": "Fixing bugs", "option2": "Modifying code at runtime", "option3": "Fixing monkeys", "option4": "Creating patches", "correct_option": 2},
            {"text": "What is the purpose of **kwargs?", "option1": "A variable", "option2": "Keyword arguments dictionary", "option3": "A function", "option4": "A module", "correct_option": 2},
        ]
    },
    "SQL": {
        "Easy": [
            {"text": "Which keyword is used to add records?", "option1": "ADD", "option2": "INSERT", "option3": "APPEND", "option4": "PUSH", "correct_option": 2},
            {"text": "Which keyword is used to modify records?", "option1": "MODIFY", "option2": "CHANGE", "option3": "UPDATE", "option4": "ALTER", "correct_option": 3},
            {"text": "What does NULL mean in SQL?", "option1": "Empty string", "option2": "Zero", "option3": "No value", "option4": "Space", "correct_option": 3},
            {"text": "Which keyword is used to sort results?", "option1": "SORT", "option2": "ORDER BY", "option3": "ARRANGE", "option4": "GROUP", "correct_option": 2},
            {"text": "What is the correct SELECT syntax?", "option1": "SELECT * FROM table WHERE condition", "option2": "FETCH * FROM table WHERE condition", "option3": "GET * FROM table WHERE condition", "option4": "RETRIEVE * FROM table WHERE condition", "correct_option": 1},
            {"text": "Which SQL function returns the average?", "option1": "MEAN()", "option2": "AVERAGE()", "option3": "AVG()", "option4": "MEDIAN()", "correct_option": 3},
            {"text": "What does SQL stand for?", "option1": "Structured Query Language", "option2": "Simple Query Language", "option3": "Standard Query Language", "option4": "System Query Language", "correct_option": 1},
            {"text": "Which command is used to retrieve data?", "option1": "INSERT", "option2": "SELECT", "option3": "UPDATE", "option4": "DELETE", "correct_option": 2},
            {"text": "What is a primary key?", "option1": "A unique identifier", "option2": "A foreign key", "option3": "A column name", "option4": "A table name", "correct_option": 1},
            {"text": "What does WHERE clause do?", "option1": "Filters rows", "option2": "Groups rows", "option3": "Orders rows", "option4": "Joins tables", "correct_option": 1},
        ],
        "Medium": [
            {"text": "What is the difference between DELETE and DROP?", "option1": "DELETE removes rows, DROP removes table", "option2": "No difference", "option3": "DELETE removes table", "option4": "Both are same", "correct_option": 1},
            {"text": "What does JOIN do?", "option1": "Combines rows from multiple tables", "option2": "Deletes tables", "option3": "Creates tables", "option4": "Updates tables", "correct_option": 1},
            {"text": "What is a foreign key?", "option1": "References another table's primary key", "option2": "A primary key", "option3": "A unique key", "option4": "A column name", "correct_option": 1},
            {"text": "What does GROUP BY do?", "option1": "Groups rows with same values", "option2": "Orders rows", "option3": "Filters rows", "option4": "Joins tables", "correct_option": 1},
            {"text": "What is the purpose of ORDER BY?", "option1": "To sort results", "option2": "To filter results", "option3": "To group results", "option4": "To join tables", "correct_option": 1},
            {"text": "What does COUNT() function do?", "option1": "Counts rows", "option2": "Counts columns", "option3": "Counts tables", "option4": "Counts databases", "correct_option": 1},
            {"text": "What is the difference between INNER JOIN and LEFT JOIN?", "option1": "INNER returns common rows, LEFT includes unmatched left rows", "option2": "No difference", "option3": "LEFT is faster", "option4": "INNER uses more memory", "correct_option": 1},
            {"text": "What does DISTINCT do?", "option1": "Removes duplicates", "option2": "Adds duplicates", "option3": "Sorts data", "option4": "Groups data", "correct_option": 1},
            {"text": "What is a view in SQL?", "option1": "A virtual table", "option2": "A physical table", "option3": "A function", "option4": "A procedure", "correct_option": 1},
            {"text": "What does HAVING clause do?", "option1": "Filters groups", "option2": "Filters rows", "option3": "Orders rows", "option4": "Joins tables", "correct_option": 1},
        ],
        "Hard": [
            {"text": "What is a subquery?", "option1": "A query within a query", "option2": "A simple query", "option3": "A complex query", "option4": "A stored query", "correct_option": 1},
            {"text": "What is normalization in SQL?", "option1": "Organizing data to reduce redundancy", "option2": "Creating backups", "option3": "Sorting data", "option4": "Grouping data", "correct_option": 1},
            {"text": "What are the types of relationships in a database?", "option1": "One-to-One, One-to-Many, Many-to-Many", "option2": "One-to-Two, Two-to-Many", "option3": "Simple, Complex", "option4": "Primary, Foreign", "correct_option": 1},
            {"text": "What is ACID property?", "option1": "Atomicity, Consistency, Isolation, Durability", "option2": "Add, Create, Insert, Delete", "option3": "Attribute, Column, Index, Data", "option4": "Alter, Change, Integrate, Duplicate", "correct_option": 1},
            {"text": "What is indexing in SQL?", "option1": "Sorting data", "option2": "Creating shortcuts for faster retrieval", "option3": "Grouping data", "option4": "Backing up data", "correct_option": 2},
            {"text": "What is a trigger in SQL?", "option1": "A special type of stored procedure", "option2": "A function", "option3": "A view", "option4": "A procedure", "correct_option": 1},
            {"text": "What is denormalization?", "option1": "Reverse process of normalization", "option2": "Organizing data", "option3": "Creating backups", "option4": "Sorting data", "correct_option": 1},
            {"text": "What is a cursor in SQL?", "option1": "A pointer to result set", "option2": "A mouse pointer", "option3": "A function", "option4": "A variable", "correct_option": 1},
            {"text": "What is the difference between UNION and UNION ALL?", "option1": "UNION removes duplicates, UNION ALL keeps them", "option2": "No difference", "option3": "UNION ALL is faster", "option4": "Both do same thing", "correct_option": 1},
            {"text": "What is a stored procedure?", "option1": "Precompiled SQL code", "option2": "A function", "option3": "A view", "option4": "A table", "correct_option": 1},
        ]
    },
    "Data Structures": {
        "Easy": [
            {"text": "Which data structure follows LIFO principle?", "option1": "Queue", "option2": "Stack", "option3": "Array", "option4": "Tree", "correct_option": 2},
            {"text": "Which data structure follows FIFO principle?", "option1": "Stack", "option2": "Queue", "option3": "Array", "option4": "Linked List", "correct_option": 2},
            {"text": "What is the time complexity of linear search?", "option1": "O(1)", "option2": "O(n)", "option3": "O(log n)", "option4": "O(n^2)", "correct_option": 2},
            {"text": "Which data structure is used for recursion?", "option1": "Queue", "option2": "Stack", "option3": "Heap", "option4": "Tree", "correct_option": 2},
            {"text": "What is the advantage of hash table?", "option1": "Sorted data", "option2": "Fast lookup", "option3": "Less memory", "option4": "Simple implementation", "correct_option": 2},
            {"text": "What is an array?", "option1": "Collection of similar data types", "option2": "A function", "option3": "A variable", "option4": "A pointer", "correct_option": 1},
            {"text": "What is linked list?", "option1": "Collection of nodes connected by pointers", "option2": "An array", "option3": "A stack", "option4": "A queue", "correct_option": 1},
            {"text": "What is the time complexity of accessing array element?", "option1": "O(1)", "option2": "O(n)", "option3": "O(log n)", "option4": "O(n^2)", "correct_option": 1},
            {"text": "What is binary search?", "option1": "Searching in sorted array", "option2": "Searching in unsorted array", "option3": "Searching in linked list", "option4": "Searching in tree", "correct_option": 1},
            {"text": "What is bubble sort?", "option1": "Sorting algorithm", "option2": "Searching algorithm", "option3": "Hashing algorithm", "option4": "Compression algorithm", "correct_option": 1},
        ],
        "Medium": [
            {"text": "What is binary tree?", "option1": "Tree with at most 2 children per node", "option2": "Tree with exactly 2 children", "option3": "Linear structure", "option4": "An array", "correct_option": 1},
            {"text": "What is height of balanced binary tree with n nodes?", "option1": "O(1)", "option2": "O(n)", "option3": "O(log n)", "option4": "O(n^2)", "correct_option": 3},
            {"text": "What is hashing?", "option1": "Technique to map data to array indices", "option2": "Sorting algorithm", "option3": "Searching algorithm", "option4": "Tree traversal", "correct_option": 1},
            {"text": "What is the worst-case time complexity of quicksort?", "option1": "O(n log n)", "option2": "O(n)", "option3": "O(n^2)", "option4": "O(log n)", "correct_option": 3},
            {"text": "What is space complexity?", "option1": "Time taken by algorithm", "option2": "Memory used by algorithm", "option3": "Number of operations", "option4": "Number of variables", "correct_option": 2},
            {"text": "What is time complexity of insertion in linked list?", "option1": "O(1)", "option2": "O(n)", "option3": "O(log n)", "option4": "O(n^2)", "correct_option": 1},
            {"text": "What is graph?", "option1": "Collection of nodes and edges", "option2": "A tree", "option3": "An array", "option4": "A queue", "correct_option": 1},
            {"text": "What is BFS?", "option1": "Breadth First Search", "option2": "Binary First Search", "option3": "Back First Search", "option4": "Bottom First Search", "correct_option": 1},
            {"text": "What is DFS?", "option1": "Depth First Search", "option2": "Data First Search", "option3": "Direct First Search", "option4": "Double First Search", "correct_option": 1},
            {"text": "What is dynamic programming?", "option1": "Solving overlapping subproblems", "option2": "Programming style", "option3": "Memory allocation", "option4": "Variable declaration", "correct_option": 1},
        ],
        "Hard": [
            {"text": "What is AVL tree?", "option1": "Self-balancing binary search tree", "option2": "Regular binary tree", "option3": "Array", "option4": "Linked list", "correct_option": 1},
            {"text": "What is Red-Black tree?", "option1": "Self-balancing binary search tree", "option2": "Tree with red and black nodes", "option3": "Regular tree", "option4": "Graph", "correct_option": 1},
            {"text": "What is Dijkstra's algorithm used for?", "option1": "Sorting", "option2": "Finding shortest path", "option3": "Searching", "option4": "Hashing", "correct_option": 2},
            {"text": "What is Fibonacci heap?", "option1": "Advanced data structure", "option2": "Regular heap", "option3": "Array", "option4": "Tree", "correct_option": 1},
            {"text": "What is suffix array?", "option1": "Array of suffixes of a string", "option2": "Regular array", "option3": "Linked list", "option4": "Tree", "correct_option": 1},
            {"text": "What is trie data structure?", "option1": "Tree for storing strings", "option2": "Regular tree", "option3": "Array", "option4": "Linked list", "correct_option": 1},
            {"text": "What is segment tree?", "option1": "Tree for range queries", "option2": "Regular tree", "option3": "Binary tree", "option4": "Balanced tree", "correct_option": 1},
            {"text": "What is B-tree?", "option1": "Self-balancing search tree", "option2": "Binary tree", "option3": "Array", "option4": "Linked list", "correct_option": 1},
            {"text": "What is topological sort?", "option1": "Sorting DAG linearly", "option2": "Regular sorting", "option3": "Searching algorithm", "option4": "Hashing algorithm", "correct_option": 1},
            {"text": "What is Kruskal's algorithm?", "option1": "Finding minimum spanning tree", "option2": "Sorting algorithm", "option3": "Searching algorithm", "option4": "Hashing algorithm", "correct_option": 1},
        ]
    },
}

with app.app_context():
    total_added = 0
    
    for category_name, difficulties in all_questions.items():
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            print(f"Category {category_name} not found")
            continue
        
        for difficulty, questions_list in difficulties.items():
            for q_data in questions_list:
                existing = Question.query.filter_by(
                    text=q_data['text'],
                    category_id=category.id
                ).first()
                
                if not existing:
                    question = Question(
                        text=q_data['text'],
                        option1=q_data['option1'],
                        option2=q_data['option2'],
                        option3=q_data['option3'],
                        option4=q_data['option4'],
                        correct_option=q_data['correct_option'],
                        difficulty=difficulty,
                        category_id=category.id
                    )
                    db.session.add(question)
                    total_added += 1
    
    db.session.commit()
    print(f"\nTotal new questions added: {total_added}")
    
    # Final verification
    print("\n" + "="*60)
    print("FINAL COUNT - HAR CATEGORY ME 10-10 QUESTIONS:")
    print("="*60)
    
    for cat in Category.query.all():
        print(f"\n{cat.name}:")
        for diff in ["Easy", "Medium", "Hard"]:
            count = Question.query.filter_by(
                category_id=cat.id,
                difficulty=diff
            ).count()
            print(f"  {diff}: {count} questions")
        
        total = Question.query.filter_by(category_id=cat.id).count()
        print(f"  TOTAL: {total} questions")
