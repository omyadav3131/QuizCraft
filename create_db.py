# create_db.py
from app import create_app, db
from app.models import User, Category, Role

app = create_app()

with app.app_context():
    print("Creating database...")
    db.create_all()

    # Create default categories
    default_categories = [
        "Quantitative Aptitude",
        "Logical Reasoning",
        "General Knowledge",
        "C Programming",
        "C++ Programming",
        "Java Programming",
        "Python Programming",
        "SQL",
        "Data Structures"
    ]

    for name in default_categories:
        exists = Category.query.filter_by(name=name).first()
        if not exists:
            db.session.add(Category(name=name))

    # Create admin user
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", email="admin@quiz.com")
        admin.set_password("admin123")
        admin.role = Role.ADMIN
        db.session.add(admin)

    db.session.commit()

    print("Database created successfully!")
    print("Admin login → username: admin | password: admin123")
