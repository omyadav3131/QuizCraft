"""
scripts/seed_demo_mock.py
Idempotent script to seed 'DEMO Mock Test' for local development & smoke testing.
Refuses to execute if DATABASE_URL points to a non-local/production database.
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

    # Reject any PostgreSQL, Supabase, or external host
    if any(keyword in db_uri_lower for keyword in ['postgres', 'postgresql', 'supabase.co', 'render.com', 'neon.tech', 'cockroach']):
        print(f"[SECURITY ERROR] DATABASE_URL points to an external/production database: {db_uri}")
        print("Refusing to seed. This script must ONLY run against a local SQLite database.")
        sys.exit(1)

    if not db_uri_lower.startswith('sqlite'):
        print(f"[SECURITY ERROR] Non-SQLite database detected ({db_uri}). Aborting for safety.")
        sys.exit(1)

    print(f"[OK] Verified local SQLite database: {db_uri}")


def seed_demo_mock():
    verify_local_database()

    app = create_app()
    with app.app_context():
        # Ensure database tables exist
        db.create_all()

        # Idempotent check for existing DEMO test
        demo_test = MockTest.query.filter_by(title="DEMO Mock Test", company_name="Demo").first()
        if not demo_test:
            demo_test = MockTest(
                company_name="Demo",
                title="DEMO Mock Test",
                description="Official practice mock assessment for smoke testing Phase A & B.",
                duration_minutes=30,
                is_active=True,
                allow_multiple_attempts=False
            )
            db.session.add(demo_test)
            db.session.commit()
            print(f"[CREATED] MockTest ID {demo_test.id}: 'DEMO Mock Test'")
        else:
            print(f"[EXISTS] MockTest ID {demo_test.id}: 'DEMO Mock Test'")

        # Section 1: Numerical Ability
        sec_num = MockSection.query.filter_by(test_id=demo_test.id, name="Numerical Ability").first()
        if not sec_num:
            sec_num = MockSection(
                test_id=demo_test.id,
                name="Numerical Ability",
                order=1,
                num_questions=3,
                section_minutes=15
            )
            db.session.add(sec_num)
            db.session.commit()
            print(f"  [CREATED] Section: Numerical Ability (ID {sec_num.id})")
        else:
            print(f"  [EXISTS] Section: Numerical Ability (ID {sec_num.id})")

        # Section 2: Verbal Ability
        sec_verb = MockSection.query.filter_by(test_id=demo_test.id, name="Verbal Ability").first()
        if not sec_verb:
            sec_verb = MockSection(
                test_id=demo_test.id,
                name="Verbal Ability",
                order=2,
                num_questions=3,
                section_minutes=15
            )
            db.session.add(sec_verb)
            db.session.commit()
            print(f"  [CREATED] Section: Verbal Ability (ID {sec_verb.id})")
        else:
            print(f"  [EXISTS] Section: Verbal Ability (ID {sec_verb.id})")

        # Numerical Ability Questions (3 Original questions)
        num_questions = [
            {
                "text": "A shopkeeper sells an article at a profit of 20%. If the cost price is Rs. 250, what is the selling price?",
                "option1": "Rs. 280",
                "option2": "Rs. 300",
                "option3": "Rs. 320",
                "option4": "Rs. 350",
                "correct_option": 2,
                "explanation": "Selling Price = Cost Price * (1 + Profit%) = 250 * 1.20 = Rs. 300.",
                "marks": 1
            },
            {
                "text": "If a train travels at 72 km/h, how many meters does it cover in 25 seconds?",
                "option1": "450 m",
                "option2": "500 m",
                "option3": "550 m",
                "option4": "600 m",
                "correct_option": 2,
                "explanation": "72 km/h = 72 * (5/18) = 20 m/s. Distance = Speed * Time = 20 * 25 = 500 m.",
                "marks": 1
            },
            {
                "text": "The ratio of two numbers is 3:5 and their sum is 160. What is the smaller number?",
                "option1": "60",
                "option2": "70",
                "option3": "80",
                "option4": "100",
                "correct_option": 1,
                "explanation": "Each unit = 160 / (3 + 5) = 20. Smaller number = 3 * 20 = 60.",
                "marks": 1
            }
        ]

        for q_data in num_questions:
            existing_q = MockQuestion.query.filter_by(section_id=sec_num.id, text=q_data["text"]).first()
            if not existing_q:
                q = MockQuestion(section_id=sec_num.id, **q_data)
                db.session.add(q)
                print(f"    [ADDED] Numerical Q: {q_data['text'][:40]}...")
            else:
                print(f"    [EXISTS] Numerical Q: {q_data['text'][:40]}...")

        # Verbal Ability Questions (3 Original questions)
        verbal_questions = [
            {
                "text": "Choose the most appropriate synonym for 'CANDID':",
                "option1": "Deceptive",
                "option2": "Straightforward and Frank",
                "option3": "Hesitant",
                "option4": "Hostile",
                "correct_option": 2,
                "explanation": "Candid means truthful, frank, and open in speech or expression.",
                "marks": 1
            },
            {
                "text": "Identify the grammatically correct sentence:",
                "option1": "Neither of the two candidates have submitted their resume.",
                "option2": "Neither of the two candidates has submitted their resume.",
                "option3": "Neither of the two candidates were submitted resume.",
                "option4": "Neither candidates has submitted resume.",
                "correct_option": 2,
                "explanation": "'Neither' as a singular subject takes the singular verb 'has'.",
                "marks": 1
            },
            {
                "text": "Choose the correct antonym for 'EPHEMERAL':",
                "option1": "Transient",
                "option2": "Short-lived",
                "option3": "Permanent and Enduring",
                "option4": "Frail",
                "correct_option": 3,
                "explanation": "Ephemeral means lasting for a very short time; its antonym is permanent or enduring.",
                "marks": 1
            }
        ]

        for q_data in verbal_questions:
            existing_q = MockQuestion.query.filter_by(section_id=sec_verb.id, text=q_data["text"]).first()
            if not existing_q:
                q = MockQuestion(section_id=sec_verb.id, **q_data)
                db.session.add(q)
                print(f"    [ADDED] Verbal Q: {q_data['text'][:40]}...")
            else:
                print(f"    [EXISTS] Verbal Q: {q_data['text'][:40]}...")

        db.session.commit()
        print(f"\n[SUCCESS] Local DEMO Mock Test seeded successfully (ID: {demo_test.id}).")
        return demo_test.id


if __name__ == '__main__':
    seed_demo_mock()
