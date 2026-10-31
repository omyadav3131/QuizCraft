"""
scripts/seed_tcs_mock.py
Idempotent script to seed 'TCS NQT Style Mock' for local development.
Refuses to execute if DATABASE_URL points to a non-local/production database.
3 sections: Numerical Ability (10 Qs), Verbal Ability (10 Qs), Reasoning Ability (10 Qs).
All original questions with mathematically derived solutions and verified explanations.
"""

import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from app import create_app, db
from app.models import MockTest, MockSection, MockQuestion


def verify_local_database():
    """Safety check: strictly abort if connected to non-local DB."""
    db_uri = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI or ''
    db_uri_lower = db_uri.lower()

    if any(keyword in db_uri_lower for keyword in ['postgres', 'postgresql', 'supabase.co', 'render.com', 'neon.tech', 'cockroach']):
        print(f"[SECURITY ERROR] DATABASE_URL points to an external/production database: {db_uri}")
        print("Refusing to seed. This script must ONLY run against a local SQLite database.")
        sys.exit(1)

    if not db_uri_lower.startswith('sqlite'):
        print(f"[SECURITY ERROR] Non-SQLite database detected ({db_uri}). Aborting for safety.")
        sys.exit(1)

    print(f"[OK] Verified local SQLite database: {db_uri}")


TCS_QUESTIONS_DATA = {
    "Numerical Ability": [
        {
            "text": "A retailer marks the price of an article 25% above its cost price of ₹4,000. If he sells it after offering a 12% discount on the marked price, what is his profit in rupees?",
            "option1": "₹360",
            "option2": "₹400",
            "option3": "₹440",
            "option4": "₹480",
            "correct_option": 2,
            "explanation": "Marked Price = ₹4,000 × 1.25 = ₹5,000. Selling Price = ₹5,000 × (1 - 0.12) = ₹5,000 × 0.88 = ₹4,400. Profit = Selling Price - Cost Price = ₹4,400 - ₹4,000 = ₹400."
        },
        {
            "text": "Pipe A can fill a tank in 12 hours, and Pipe B can fill it in 15 hours. A drainage Pipe C can empty the full tank in 20 hours. If all three pipes are opened simultaneously into an empty tank, how many hours will it take to fill the tank completely?",
            "option1": "8 hours",
            "option2": "10 hours",
            "option3": "12 hours",
            "option4": "15 hours",
            "correct_option": 2,
            "explanation": "In 1 hour, portion of the tank filled = (1/12) + (1/15) - (1/20) = (5 + 4 - 3)/60 = 6/60 = 1/10. Therefore, the time required to fill the tank completely = 1 / (1/10) = 10 hours."
        },
        {
            "text": "A train traveling at a constant speed of 72 km/h crosses a 280-meter long tunnel in 24 seconds. What is the length of the train in meters?",
            "option1": "180 m",
            "option2": "200 m",
            "option3": "220 m",
            "option4": "240 m",
            "correct_option": 2,
            "explanation": "Speed in m/s = 72 × (5/18) = 20 m/s. Total distance traveled in 24 seconds = 20 m/s × 24 s = 480 meters. Since Total distance = Train length + Tunnel length, Train length = 480 m - 280 m = 200 meters."
        },
        {
            "text": "A vessel contains 60 liters of a mixture of milk and water in the ratio 3 : 2. How many liters of water must be added to the mixture so that the ratio of milk to water becomes 1 : 1?",
            "option1": "8 liters",
            "option2": "10 liters",
            "option3": "12 liters",
            "option4": "15 liters",
            "correct_option": 3,
            "explanation": "Initial milk = 60 × (3 / 5) = 36 liters; initial water = 60 × (2 / 5) = 24 liters. To achieve a 1 : 1 ratio, the quantity of water must equal the quantity of milk (36 liters). Water to be added = 36 - 24 = 12 liters."
        },
        {
            "text": "A sum of ₹8,000 is invested at an annual interest rate of 10% compounded annually. What is the compound interest earned at the end of 2 years?",
            "option1": "₹1,600",
            "option2": "₹1,680",
            "option3": "₹1,720",
            "option4": "₹1,800",
            "correct_option": 2,
            "explanation": "Amount = P(1 + R/100)^T = 8000 × (1 + 10/100)^2 = 8000 × (1.10)^2 = 8000 × 1.21 = ₹9,680. Compound Interest = Amount - Principal = 9,680 - 8,000 = ₹1,680."
        },
        {
            "text": "The average age of a group of 6 colleagues is 35 years. When one member leaves and is replaced by a new colleague aged 28 years, the average age of the group becomes 33 years. What was the age of the colleague who left?",
            "option1": "36 years",
            "option2": "38 years",
            "option3": "40 years",
            "option4": "42 years",
            "correct_option": 3,
            "explanation": "Initial total age of the 6 colleagues = 6 × 35 = 210 years. New total age after replacement = 6 × 33 = 198 years. Let X be the age of the colleague who left. Then: 210 - X + 28 = 198 => 238 - X = 198 => X = 238 - 198 = 40 years."
        },
        {
            "text": "Find the least number which when divided by 12, 15, and 20 leaves a remainder of 7 in each case.",
            "option1": "57",
            "option2": "67",
            "option3": "77",
            "option4": "127",
            "correct_option": 2,
            "explanation": "The required least number is LCM(12, 15, 20) + Remainder. LCM(12, 15, 20) = 60. Therefore, the least number = 60 + 7 = 67."
        },
        {
            "text": "A box contains 5 red balls, 4 blue balls, and 3 green balls. If two balls are drawn at random one after another without replacement, what is the probability that both balls are blue?",
            "option1": "1/11",
            "option2": "1/12",
            "option3": "2/33",
            "option4": "3/22",
            "correct_option": 1,
            "explanation": "Total number of balls = 5 + 4 + 3 = 12. Probability of first ball being blue = 4 / 12 = 1 / 3. Remaining blue balls = 3; remaining total balls = 11. Probability of second ball being blue = 3 / 11. Combined probability = (4 / 12) × (3 / 11) = 12 / 132 = 1 / 11."
        },
        {
            "text": "In a right-angled triangle, the hypotenuse measures 25 cm and the base measures 24 cm. What is the area of the triangle in square centimeters?",
            "option1": "72 sq.cm",
            "option2": "84 sq.cm",
            "option3": "96 sq.cm",
            "option4": "168 sq.cm",
            "correct_option": 2,
            "explanation": "By Pythagoras theorem, Height = √(Hypotenuse² - Base²) = √(25² - 24²) = √(625 - 576) = √49 = 7 cm. Area = (1/2) × Base × Height = (1/2) × 24 cm × 7 cm = 12 × 7 = 84 sq.cm."
        },
        {
            "text": "If 2x + 3y = 23 and 3x + 2y = 27, what is the value of (x + y)?",
            "option1": "8",
            "option2": "9",
            "option3": "10",
            "option4": "11",
            "correct_option": 3,
            "explanation": "Adding the two equations directly: (2x + 3y) + (3x + 2y) = 23 + 27 => 5x + 5y = 50 => 5(x + y) = 50 => x + y = 10. (Alternatively, solving gives x = 7 and y = 3, so x + y = 10)."
        }
    ],
    "Verbal Ability": [
        {
            "text": "Choose the word most nearly SIMILAR in meaning (SYNONYM) to 'TRANSPARENT' as used in the sentence: 'The auditor found that the company's financial records were completely transparent, leaving no room for suspicion.'",
            "option1": "Ambiguous",
            "option2": "Clear",
            "option3": "Complex",
            "option4": "Deceptive",
            "correct_option": 2,
            "explanation": "'Transparent' in this context means easily understood, clear, and free from deceit or concealment. 'Clear' is the exact synonym."
        },
        {
            "text": "Select the word OPPOSITE in meaning (ANTONYM) to 'FRUGAL' as used in the sentence: 'Her frugal lifestyle allowed her to save a significant portion of her monthly salary.'",
            "option1": "Thrifty",
            "option2": "Extravagant",
            "option3": "Economical",
            "option4": "Prudent",
            "correct_option": 2,
            "explanation": "'Frugal' means careful and economical in spending resources. Its direct opposite is 'Extravagant' (spending money wastefully or excessively)."
        },
        {
            "text": "Choose the grammatically correct sentence from the options below:",
            "option1": "Neither the manager nor the employees was present at the safety briefing.",
            "option2": "Neither the manager nor the employees were present at the safety briefing.",
            "option3": "Neither the manager nor the employees is present at the safety briefing.",
            "option4": "Neither the manager nor the employees has been present at the safety briefing.",
            "correct_option": 2,
            "explanation": "When two subjects are connected by 'neither... nor', the verb must agree with the closer subject. Here, 'employees' is plural, requiring the plural verb 'were'."
        },
        {
            "text": "Identify the sentence that does NOT contain a misplaced or dangling modifier:",
            "option1": "Walking through the park, the fallen leaves covered the path.",
            "option2": "Having completed the project, the report was submitted by the analyst.",
            "option3": "Having completed the project, the analyst submitted the report.",
            "option4": "Running for the train, his wallet fell from his pocket.",
            "correct_option": 3,
            "explanation": "In option 3, the introductory participle phrase 'Having completed the project' correctly modifies the agent who did the action ('the analyst'). In options 1, 2, and 4, the participle incorrectly modifies 'the leaves', 'the report', and 'his wallet'."
        },
        {
            "text": "Select the appropriate preposition to complete the sentence: 'She is very fond ______ classical music.'",
            "option1": "of",
            "option2": "about",
            "option3": "with",
            "option4": "for",
            "correct_option": 1,
            "explanation": "The adjective 'fond' is strictly followed by the preposition 'of' ('to be fond of something'). 'About', 'with', and 'for' are grammatically incorrect in this context."
        },
        {
            "text": "What is the true meaning of the idiom 'to burn the midnight oil'?",
            "option1": "To waste fuel or resources carelessly",
            "option2": "To work or study late into the night",
            "option3": "To cause accidental damage by negligence",
            "option4": "To wake up earlier than usual",
            "correct_option": 2,
            "explanation": "'To burn the midnight oil' is an established English idiom meaning to stay up working or studying late into the night."
        },
        {
            "text": "Read the sentence and find which part contains a grammatical error: 'Despite of (A) / all his preparations, (B) / he could not qualify (C) / for the final round. (D)'",
            "option1": "Despite of (A)",
            "option2": "all his preparations (B)",
            "option3": "he could not qualify (C)",
            "option4": "for the final round (D)",
            "correct_option": 1,
            "explanation": "'Despite' is a preposition that never takes 'of'. The correct phrase is either 'Despite all his preparations' or 'In spite of all his preparations'."
        },
        {
            "text": "Arrange the sentences into a coherent paragraph:\nP: This real-time analysis helps prevent potential fraudulent transactions.\nQ: Banks process millions of digital payment requests every second.\nR: Advanced machine learning algorithms immediately scan each transaction for suspicious patterns.\nS: These high transaction volumes demand automated security mechanisms.",
            "option1": "Q-S-R-P",
            "option2": "Q-P-S-R",
            "option3": "S-Q-P-R",
            "option4": "P-Q-S-R",
            "correct_option": 1,
            "explanation": "Q introduces the premise (millions of payments). S links the volume to need for automated security. R specifies the mechanism (machine learning algorithms scan transactions). P concludes with the outcome (preventing fraudulent transactions). The logical flow is Q-S-R-P."
        },
        {
            "text": "Which option represents the correct passive transformation of: 'The committee approved the revised proposal yesterday.'",
            "option1": "The revised proposal was approved by the committee yesterday.",
            "option2": "The revised proposal has been approved by the committee yesterday.",
            "option3": "The revised proposal had been approved by the committee yesterday.",
            "option4": "The revised proposal is approved by the committee yesterday.",
            "correct_option": 1,
            "explanation": "The active sentence is in Simple Past ('approved'). The passive rule for Simple Past is 'was/were + past participle' ('was approved')."
        },
        {
            "text": "Read the passage: 'Renewable energy adoption has accelerated significantly over the past decade. However, the intermittent nature of solar and wind energy means that grid reliability still requires either substantial battery storage infrastructure or backup generation capacity.' What can be directly inferred from the passage?",
            "option1": "Solar and wind energy are unsuitable for modern power grids.",
            "option2": "Renewable energy sources alone cannot guarantee uninterrupted grid power without energy storage or backup systems.",
            "option3": "Battery storage systems are cheaper than conventional backup power plants.",
            "option4": "Global energy demand has declined as a result of renewable energy adoption.",
            "correct_option": 2,
            "explanation": "The passage directly explains that due to intermittent generation, grid reliability cannot be maintained without storage or backup, directly supporting Option 2."
        }
    ],
    "Reasoning Ability": [
        {
            "text": "What is the next number in the geometric series: 7, 14, 28, 56, 112, ___?",
            "option1": "168",
            "option2": "196",
            "option3": "224",
            "option4": "248",
            "correct_option": 3,
            "explanation": "Each term is obtained by multiplying the preceding term by 2: 7×2=14, 14×2=28, 28×2=56, 56×2=112, 112×2=224."
        },
        {
            "text": "In a certain code language, if 'CLOUD' is coded as 'DMPVE', how will 'TIGER' be coded in that same language?",
            "option1": "UJHFS",
            "option2": "VKIGT",
            "option3": "UJGES",
            "option4": "TIGFS",
            "correct_option": 1,
            "explanation": "Each letter is shifted forward by 1 position in the alphabet (+1 shift): T(+1)→U, I(+1)→J, G(+1)→H, E(+1)→F, R(+1)→S. Hence, 'TIGER' becomes 'UJHFS'."
        },
        {
            "text": "Pointing to a photograph of a boy, Suresh said: 'He is the only son of my father's only son.' How is the boy related to Suresh?",
            "option1": "Brother",
            "option2": "Son",
            "option3": "Nephew",
            "option4": "Uncle",
            "correct_option": 2,
            "explanation": "Suresh is a male speaker. 'My father's only son' refers to Suresh himself. The statement therefore means: 'He is the only son of Suresh.' Thus, the boy is Suresh's son."
        },
        {
            "text": "Ankit starts from point P and walks 20 meters North. He turns right and walks 15 meters, then turns right again and walks 20 meters. Finally, he turns left and walks 10 meters to reach point Q. In which direction and at what straight-line distance is point Q from point P?",
            "option1": "25 meters East",
            "option2": "25 meters West",
            "option3": "35 meters East",
            "option4": "15 meters North",
            "correct_option": 1,
            "explanation": "Vertical displacement = +20 m (North) - 20 m (South) = 0 m. Horizontal displacement = +15 m (East) + 10 m (East) = +25 meters East. Point Q is 25 meters due East of point P."
        },
        {
            "text": "Statements:\nI. All roses are flowers.\nII. All flowers are plants.\nConclusions:\n1. All roses are plants.\n2. Some plants are roses.\nWhich conclusion(s) logically follow?",
            "option1": "Only conclusion 1 follows",
            "option2": "Only conclusion 2 follows",
            "option3": "Neither conclusion 1 nor 2 follows",
            "option4": "Both conclusions 1 and 2 follow",
            "correct_option": 4,
            "explanation": "Roses ⊆ Flowers ⊆ Plants. Transitivity implies Roses ⊆ Plants, so Conclusion 1 definitely follows. Since the set of roses is non-empty, Plants ∩ Roses is non-empty, so Conclusion 2 ('Some plants are roses') also definitely follows. Hence, both follow."
        },
        {
            "text": "In a row of 40 students facing North, Priya is 15th from the left end. What is Priya's position from the right end of the row?",
            "option1": "24th",
            "option2": "25th",
            "option3": "26th",
            "option4": "27th",
            "correct_option": 3,
            "explanation": "Position from Right = Total Students - Position from Left + 1 = 40 - 15 + 1 = 26th."
        },
        {
            "text": "Select the pair that expresses a relationship most similar to that expressed in the original pair:\nAUTHOR : BOOK :: ?",
            "option1": "DOCTOR : MEDICINE",
            "option2": "COMPOSER : SYMPHONY",
            "option3": "ACTOR : THEATER",
            "option4": "TEACHER : CLASSROOM",
            "correct_option": 2,
            "explanation": "An author creates a book (Creator : Intellectual Creation). Similarly, a composer creates a symphony. A doctor does not create medicine, an actor performs in a theater, and a teacher teaches in a classroom."
        },
        {
            "text": "Four letter-clusters are given below. Three are alike in a certain manner and one is different. Select the odd one out:",
            "option1": "CEG",
            "option2": "KMO",
            "option3": "PRT",
            "option4": "UWZ",
            "correct_option": 4,
            "explanation": "In CEG (C+2=E, E+2=G), KMO (K+2=M, M+2=O), and PRT (P+2=R, R+2=T), the consecutive letters have an alphabet difference of +2. In UWZ, U+2=W, but W+3=Z. Therefore, UWZ is the odd one out."
        },
        {
            "text": "At 4:20, what is the acute angle between the hour hand and the minute hand of an analog clock?",
            "option1": "0°",
            "option2": "10°",
            "option3": "15°",
            "option4": "20°",
            "correct_option": 2,
            "explanation": "Hour hand angle from 12:00 = 4 × 30° + 20 × 0.5° = 120° + 10° = 130°. Minute hand angle from 12:00 = 20 × 6° = 120°. The angle between them = |130° - 120°| = 10°."
        },
        {
            "text": "Five friends—A, B, C, D, and E—are seated in a row facing North.\n1. C sits in the exact middle of the row.\n2. A sits immediately to the left of C.\n3. B sits at the extreme right end.\n4. E sits immediately to the left of B.\nWho is sitting at the extreme left end of the row?",
            "option1": "A",
            "option2": "B",
            "option3": "D",
            "option4": "E",
            "correct_option": 3,
            "explanation": "Row positions 1 to 5 from left to right: Condition 1 places C at position 3. Condition 2 places A at position 2 (immediate left of C). Condition 3 places B at position 5 (extreme right). Condition 4 places E at position 4 (immediate left of B). The only remaining person D must sit at position 1 (extreme left end)."
        }
    ]
}


def seed_tcs_mock():
    verify_local_database()

    app = create_app()
    with app.app_context():
        db.create_all()

        test_title = "TCS NQT Style Mock"
        company = "TCS"

        test = MockTest.query.filter_by(title=test_title, company_name=company).first()
        if not test:
            test = MockTest(
                company_name=company,
                title=test_title,
                description="Simulated TCS NQT placement examination featuring 3 core sections: Numerical Ability, Verbal Ability, and Reasoning Ability. Zero negative marking, single-attempt rule, and proctoring discipline monitoring.",
                duration_minutes=45,
                is_active=True,
                allow_multiple_attempts=False
            )
            db.session.add(test)
            db.session.commit()
            print(f"[OK] Created mock test: '{test_title}' (ID: {test.id})")
        else:
            test.duration_minutes = 45
            test.is_active = True
            test.allow_multiple_attempts = False
            db.session.commit()
            print(f"[INFO] Mock test '{test_title}' already exists (ID: {test.id}). Updating sections.")

        section_order = {
            "Numerical Ability": 1,
            "Verbal Ability": 2,
            "Reasoning Ability": 3
        }

        total_questions_seeded = 0

        for section_name, questions in TCS_QUESTIONS_DATA.items():
            section = MockSection.query.filter_by(test_id=test.id, name=section_name).first()
            if not section:
                section = MockSection(
                    test_id=test.id,
                    name=section_name,
                    order=section_order[section_name],
                    num_questions=len(questions),
                    section_minutes=15
                )
                db.session.add(section)
                db.session.commit()
                print(f"  [OK] Created section: '{section_name}' (ID: {section.id})")
            else:
                section.order = section_order[section_name]
                section.num_questions = len(questions)
                section.section_minutes = 15
                db.session.commit()
                # Clean up existing questions for this section if any to ensure clean updated reload
                MockQuestion.query.filter_by(section_id=section.id).delete()
                db.session.commit()
                print(f"  [OK] Section '{section_name}' refreshed for clean re-insertion.")

            for q_data in questions:
                q = MockQuestion(
                    section_id=section.id,
                    text=q_data['text'],
                    option1=q_data['option1'],
                    option2=q_data['option2'],
                    option3=q_data['option3'],
                    option4=q_data['option4'],
                    correct_option=q_data['correct_option'],
                    explanation=q_data['explanation'],
                    marks=1
                )
                db.session.add(q)
                total_questions_seeded += 1

        db.session.commit()
        print(f"\n[SUCCESS] Seeded {total_questions_seeded} questions across 3 sections for '{test_title}'.")


if __name__ == '__main__':
    seed_tcs_mock()
