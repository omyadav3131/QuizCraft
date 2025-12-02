# Flask Quiz Application

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-1.1.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A fully responsive, feature-rich Quiz Application built with Python's Flask framework. This application allows users to take quizzes across multiple categories and difficulty levels, track their scores, and compete on the leaderboard. Admins can manage questions, categories, and users through a comprehensive admin panel.

## 📋 Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Database Models](#database-models)
8. [Routes & Endpoints](#routes--endpoints)
9. [Screenshots](#screenshots)
10. [Contributing](#contributing)
11. [License](#license)

## ✨ Features

### User Features
- **Authentication System**
  - User registration with email and username
  - Secure login with password hashing (Werkzeug)
  - Session management with Flask-Login
  - User profile management

- **Quiz System**
  - Multiple quiz categories
  - Three difficulty levels: Easy, Medium, Hard
  - **Points System**: Easy questions = 2 points, Medium = 4 points, Hard = 6 points per correct answer
  - Timed quizzes (10 minutes per quiz)
  - **Large, readable question box** with improved padding and font size
  - **Timer displayed outside question box** for better visibility
  - 10 questions per quiz
  - Multiple choice questions (4 options)
  - Real-time score tracking
  - Immediate result display with percentage score and total points earned
  - **Detailed Answer Review** after quiz completion:
    - Question-by-question breakdown
    - Color-coded answers (Green for correct, Red for wrong)
    - Shows your selected answer vs correct answer
    - Points earned per question displayed
    - Explanations for each question (if available)
  - Performance feedback based on score
  - Quiz attempt history saved to database
  - **Feedback form** accessible anytime via homepage button (Name, Rating 1-5, Feedback text)
  - **Feedback button** on homepage for easy access

- **Leaderboard**
  - Vertical card-style leaderboard (modern UI)
  - **Points-based ranking system** (sorted by points, then score)
  - Top 50 performers displayed
  - Medal icons for top 3 (Gold, Silver, Bronze)
  - **Category-wise leaderboards** with filter dropdown
  - Color-coded difficulty badges
  - Category and date information
  - Points displayed prominently on each card
  - API endpoint for programmatic access (`/api/leaderboard`)
  - Filters by category and difficulty (API)
  - Leaderboard button on homepage and navigation

- **Performance Dashboard**
  - Interactive performance graphs using Chart.js
  - Score trend over time (line chart)
  - Points earned over time (bar chart)
  - Performance breakdown by category (doughnut chart)
  - Performance breakdown by difficulty (bar chart)
  - Statistics cards showing total quizzes, average score, total points
  - Recent quiz attempts table
  - Accessible via "Performance Dashboard" button on homepage

### Admin Features
- **Dashboard**
  - Overview of all categories and questions
  - Total questions count
  - Category-wise question listing

- **Category Management**
  - Create new categories
  - View all categories
  - Organized question listing by category

- **Question Management**
  - Create new questions with 4 options
  - Edit existing questions
  - Delete questions
  - Bulk add questions (CSV/TXT format)
  - Set difficulty level (Easy/Medium/Hard)
  - Add explanations to questions
  - Associate questions with categories

- **User Management**
  - View all registered users
  - Create new user accounts
  - Edit user details
  - Delete users
  - Assign admin roles
  - Manage user permissions

- **Feedback Management**
  - View all user feedback and ratings
  - See feedback submissions with timestamps
  - Rating system (1-5 stars)
  - Feedback text display

- **Admin Restrictions**
  - Admins cannot play quizzes (blocked at route level)
  - Admin dashboard only shows management operations
  - Leaderboard access for admins to view rankings

## 🛠 Tech Stack

### Backend
- **Flask 1.1.2** - Web framework
- **Flask-SQLAlchemy 2.4.4** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-Migrate 2.5.3** - Database migrations
- **Flask-WTF 0.14.3** - Form handling and CSRF protection
- **Werkzeug** - Password hashing and security utilities
- **SQLite** - Database (can be easily switched to PostgreSQL/MySQL)

### Frontend
- **Bootstrap 4.0** - Responsive CSS framework
- **Font Awesome 6.0** - Icons
- **Custom CSS** - Professional styling with gradients and animations
- **Google Fonts (Raleway)** - Modern typography
- **Jinja2** - Template engine

### Development Tools
- **Alembic** - Database migration tool
- **Gunicorn** - Production WSGI server
- **Python 3.8+** - Programming language

## 📁 Project Structure

```
flask-quiz-app/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (User, Category, Question, Attempt, etc.)
│   ├── admin/               # Admin blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Admin routes (CRUD operations)
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py        # Login, Register, Logout routes
│   │   └── forms.py         # WTForms for authentication
│   ├── quiz/                # Quiz blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Quiz routes (select, start, question, result, leaderboard)
│   ├── static/
│   │   ├── css/
│   │   │   ├── professional.css      # Main theme styles
│   │   │   ├── custom.css            # Custom component styles
│   │   │   └── leaderboard_vertical.css  # Leaderboard card styles
│   │   └── images/                   # Static images
│   └── templates/
│       ├── base.html                 # Base template
│       ├── home.html                 # Home page
│       ├── admin/                    # Admin templates
│       ├── auth/                     # Auth templates (login, register)
│       └── quiz/                     # Quiz templates
├── migrations/               # Database migration files
├── config.py                # Configuration settings
├── create_db.py             # Database initialization script
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── README_RUN.md            # Quick start guide
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/thepasterover/flask-quiz-app.git
cd flask-quiz-app
```

Or download and extract the ZIP file.

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Initialize Database
```bash
python create_db.py
```

This script will:
- Create the SQLite database (`quiz.db`)
- Create default categories
- Create an admin user:
  - **Username:** `admin`
  - **Password:** `admin123`

#### 5. Run the Application
```bash
python main.py
```

The application will be available at: **http://127.0.0.1:5000**

## ⚙️ Configuration

### Environment Variables

You can set the following environment variables:

- `SECRET_KEY` - Flask secret key for session management (default: auto-generated)
- `DATABASE_URL` - Database connection string (default: SQLite)
- `FLASK_APP` - Application entry point (default: `main.py`)
- `FLASK_ENV` - Environment mode: `development` or `production`

### Database Configuration

The default configuration uses SQLite. To use PostgreSQL or MySQL, update `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/quizdb'
# or
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/quizdb'
```

## 📖 Usage

### For Users

1. **Register/Login**
   - Visit the homepage
   - Click "Register" to create an account
   - Or "Login" with existing credentials (regular users only)
   - **Admin Login**: Use separate "Admin Login" button for admin access

2. **Take a Quiz**
   - Click "Quiz" in the navigation
   - Select a category
   - Choose difficulty level (Easy/Medium/Hard)
   - Answer 10 questions within 10 minutes
   - Submit to see your score

3. **View Leaderboard**
   - Navigate to `/quiz/leaderboard` or click "Leaderboard" button on homepage
   - See top 50 performers sorted by points
   - Filter by category using dropdown
   - View points, scores, and difficulty badges
   - See rankings with medals for top 3

4. **View Detailed Results**
   - After quiz completion, see detailed answer review
   - Review all questions with your answers
   - See correct answers highlighted in green
   - See wrong answers highlighted in red
   - View points earned per question
   - Read explanations for better understanding

5. **View Performance Dashboard**
   - Click "Performance Dashboard" button on homepage
   - See interactive graphs showing:
     - Score trends over time (line chart)
     - Points earned over time (bar chart)
     - Performance by category (doughnut chart)
     - Performance by difficulty level (bar chart)
   - View statistics: Total quizzes, Average score, Total points, Avg points per quiz
   - See recent quiz attempts in a table

6. **Submit Feedback**
   - Click "Feedback" button on homepage (available before taking quiz)
   - Rate your experience (1-5 stars)
   - Share your thoughts and suggestions
   - Feedback can be submitted anytime, not just after quiz completion

### For Admins

1. **Login as Admin**
   - Click "Admin Login" button on homepage or navigation
   - Use credentials: `admin` / `admin123`
   - Regular user login page blocks admin access
   - Access admin panel after successful login

2. **Manage Categories**
   - Go to "Categories"
   - Add new categories
   - View existing categories

3. **Manage Questions**
   - Go to "Questions"
   - Add individual questions
   - Use "Bulk Add" for multiple questions
   - Edit or delete questions

4. **Manage Users**
   - Go to "Users"
   - View all users
   - Create, edit, or delete user accounts
   - Assign admin roles

5. **View Feedback**
   - Go to "Feedback" in admin dashboard
   - View all user feedback and ratings
   - See feedback submissions with timestamps

6. **View Leaderboard**
   - Admins can view leaderboard to see user rankings
   - Access via "Leaderboard" button in admin dashboard or navigation

## 🗄️ Database Models

### User
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email (optional)
- `password_hash` - Hashed password
- `role` - User role (user/admin)
- `attempts` - Relationship to Attempt model

### Category
- `id` - Primary key
- `name` - Category name (unique)
- `questions` - Relationship to Question model

### Question
- `id` - Primary key
- `text` - Question text
- `option1`, `option2`, `option3`, `option4` - Answer options
- `correct_option` - Correct option number (1-4)
- `explanation` - Optional explanation
- `category_id` - Foreign key to Category
- `difficulty` - Difficulty level (Easy/Medium/Hard)

### Attempt
- `id` - Primary key
- `user_id` - Foreign key to User
- `score` - Score achieved (number of correct answers)
- `total` - Total questions
- `points` - Total points earned based on difficulty (Easy=2, Medium=4, Hard=6 per correct answer)
- `category_id` - Foreign key to Category
- `difficulty` - Difficulty level
- `created_at` - Timestamp

### AttemptAnswer
- `id` - Primary key
- `attempt_id` - Foreign key to Attempt
- `question_id` - Foreign key to Question
- `chosen_option` - Option selected by user (1-4)
- `correct` - Boolean indicating if answer was correct
- **Note**: Used for detailed answer review on result page

### LeaderboardEntry
- `id` - Primary key
- `user_id` - Foreign key to User
- `username` - Username (denormalized)
- `score` - Score achieved (number of correct answers)
- `total` - Total questions
- `points` - Total points earned based on difficulty
- `category_id` - Foreign key to Category
- `difficulty` - Difficulty level
- `created_at` - Timestamp

### Feedback
- `id` - Primary key
- `user_id` - Foreign key to User (nullable)
- `name` - User's name
- `rating` - Rating (1-5 stars)
- `feedback_text` - Feedback text
- `created_at` - Timestamp

## 🔗 Routes & Endpoints

### Public Routes
- `GET /` - Home page

### Authentication Routes (`/auth`)
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login (regular users only, admins blocked)
- `GET/POST /auth/admin/login` - Admin login (admin users only)
- `GET /auth/logout` - User logout

### Quiz Routes (`/quiz`)
- `GET /quiz/select` - Select quiz category (requires login, admin blocked)
- `GET /quiz/start/<category_id>` - Select difficulty (requires login, admin blocked)
- `GET /quiz/start/<category_id>/<difficulty>` - Start quiz (requires login, admin blocked)
- `GET/POST /quiz/question/<q_id>` - Answer question (requires login)
- `GET /quiz/result` - View quiz result with detailed answer review and points (requires login)
- `GET /quiz/performance` - Performance dashboard with graphs and statistics (requires login, admin blocked)
- `GET /quiz/feedback` - Access feedback form page (requires login, available before quiz)
- `POST /quiz/feedback` - Submit feedback (requires login)
  - Shows question-by-question breakdown
  - Color-coded correct/wrong answers
  - Points per question displayed
  - Correct answers shown for wrong questions
- `POST /quiz/feedback` - Submit feedback after quiz (requires login)
- `GET /quiz/leaderboard` - Vertical card leaderboard sorted by points (requires login)
- `GET /quiz/leaderboard/<category_name>` - Category-wise leaderboard (requires login)
- `GET /quiz/api/leaderboard` - JSON API for leaderboard data

### Admin Routes (`/admin`) - Requires Admin Role
- `GET /admin/` - Admin dashboard (no quiz access, management only)
- `GET/POST /admin/categories` - Manage categories
- `GET/POST /admin/question/new` - Create new question
- `GET/POST /admin/question/edit/<q_id>` - Edit question
- `POST /admin/question/delete/<q_id>` - Delete question
- `GET /admin/users` - View all users
- `GET/POST /admin/user/new` - Create new user
- `GET/POST /admin/user/edit/<user_id>` - Edit user
- `POST /admin/user/delete/<user_id>` - Delete user
- `GET/POST /admin/questions/bulk-add` - Bulk add questions
- `GET /admin/feedback` - View all user feedback and ratings

## 🎨 Features in Detail

### Modern UI/UX
- Responsive design (mobile, tablet, desktop)
- Professional color scheme with gradients
- Smooth animations and transitions
- Icon-based navigation (Font Awesome)
- Card-based layouts
- Modern typography (Google Fonts)

### Security Features
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Role-based access control
- Secure admin authentication

### Performance
- SQLite for fast local development
- Optimized database queries
- Lazy loading relationships
- Efficient pagination for leaderboard

## 📸 Screenshots

*Add screenshots of your application here*

## 🐛 Known Issues & Fixes

### Fixed Issues (Latest Update)
- ✅ **Session Management Bug Fixed**: Session values are now retrieved before clearing, ensuring points and difficulty display correctly
- ✅ **Points Display Fixed**: Points now correctly calculated and displayed on result page and leaderboard
- ✅ **Answer Review Added**: Detailed question-by-question review with color coding implemented
- ✅ **Feedback Button Added**: Feedback button now visible on homepage

### Current Status
- All critical bugs have been resolved
- All requested features have been implemented

## ✨ Latest Features

- ✅ **Separate Admin Login** - Dedicated admin login page

## 🔮 Future Enhancements

- [ ] Two-person competition mode with unique codes
- [ ] Real-time synchronization for competitions (WebSockets)
- [ ] Daily automatic leaderboard updates
- [ ] Add quiz time customization
- [ ] Implement question banks
- [ ] Add quiz analytics and statistics
- [ ] Email notifications for quiz results
- [ ] Social sharing of scores
- [ ] Export quiz results as PDF
- [ ] Multiple languages support
- [ ] Dark mode theme
- [ ] Question images support
- [ ] Real-time multiplayer quizzes

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write descriptive commit messages
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

## 📝 License

This project is distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Boobalan Shettiyar**
- Email: boopalanshettiyar78@gmail.com
- GitHub: [@thepasterover](https://github.com/thepasterover)
- Project Link: [https://github.com/thepasterover/flask-quiz-app](https://github.com/thepasterover/flask-quiz-app)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for the amazing CSS framework
- Font Awesome for beautiful icons
- All contributors who helped improve this project

## 📞 Support

If you have any questions, issues, or feature requests, please:
- Open an issue on GitHub
- Contact the author via email
- Check the documentation in `README_RUN.md` for quick start guide

---

⭐ If you find this project helpful, please give it a star on GitHub!
