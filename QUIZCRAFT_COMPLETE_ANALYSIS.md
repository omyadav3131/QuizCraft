# QuizCraft — Complete Project Analysis & Documentation

> **Live URL:** [https://quizcraft-qt15.onrender.com](https://quizcraft-qt15.onrender.com)
> **Author:** Om Yadav | **GitHub:** [omyadav3131](https://github.com/omyadav3131)
> **Status:** Deployed & Live on Render
> **Last Updated:** October 25, 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Database Statistics](#database-statistics)
4. [Project Structure](#project-structure)
5. [Database Models](#database-models)
6. [All Features & Functions](#all-features--functions)
7. [URL Routes — Complete List](#url-routes--complete-list)
8. [User Flow](#user-flow)
9. [Security Features](#security-features)
10. [Issues & Bugs Found](#issues--bugs-found)
11. [Industry-Level Improvements Needed](#industry-level-improvements-needed)
12. [Priority Action Plan](#priority-action-plan)

---

## Project Overview

**QuizCraft** ek full-stack web application hai jo Flask (Python) se bana hai. Yeh platform users ko online quiz khelte hue apni knowledge test karne, performance track karne aur dusre users ke saath multiplayer competition khelte hue compete karne deta hai.

### Kya hai yeh platform?
- Category-based Quiz System — alag-alag subjects mein quiz
- Leaderboard — top scorers ka ranking
- Performance Analytics — user ka detailed progress
- Multiplayer Competition — 2 logon ke beech live quiz battle
- Admin Dashboard — questions, users, categories manage karna
- Feedback System — users se rating aur review lena

---

## Tech Stack

### Backend

| Technology | Version | Use |
|---|---|---|
| Python | 3.11 | Core Language |
| Flask | Latest | Web Framework |
| Flask-SQLAlchemy | Latest | ORM / Database |
| Flask-Login | Latest | Session & Auth |
| Flask-WTF | Latest | Forms & CSRF |
| Flask-Migrate | Latest | DB Migrations |
| Werkzeug | Latest | Password Hashing |
| Gunicorn | Latest | Production Server |

### Frontend

| Technology | Use |
|---|---|
| HTML5 | Structure |
| CSS3 + Bootstrap | Styling |
| Jinja2 | Template Engine |
| JavaScript | Client-side Logic |

### Database

| Environment | Database |
|---|---|
| Development | SQLite (quiz.db) |
| Production (Render) | PostgreSQL (via Supabase) |

### Deployment

| Service | Use |
|---|---|
| Render | Web Hosting |
| Supabase | PostgreSQL Database |
| GitHub | Version Control |

---

## Database Statistics (Current Live Data)

| Metric | Count |
|---|---|
| **Total Questions** | **300** (+20 added Oct 25) |
| **Total Categories** | **10** |
| **Registered Users** | **4** |
| **Total Quiz Attempts** | **41** |
| **Total Competitions** | **7** |

### Questions by Category & Difficulty

| Category | Easy | Medium | Hard | Total |
|---|---|---|---|---|
| Quantitative Aptitude | 10 | 10 | 10 | **30** |
| Logical Reasoning | 10 | 10 | 10 | **30** |
| General Knowledge | 10 | 10 | 10 | **30** |
| C Programming | 10 | 10 | 10 | **30** |
| C++ Programming | 10 | 10 | 10 | **30** |
| Java Programming | 10 | 10 | 10 | **30** |
| Python Programming | 10 | 10 | 10 | **30** |
| SQL | 10 | 10 | 10 | **30** |
| Data Structures | 10 | 10 | 10 | **30** |
| Computer | 10 | 10 | 10 | **30** ✅ FIXED Oct 25 |
| **TOTAL** | **101** | **100** | **100** | **300** |

> All categories now have Easy + Medium + Hard questions. Computer category completed on Oct 25.

---

## Project Structure

```
QuizCraft/
├── app/
│   ├── __init__.py              # Flask app factory, Blueprint registration
│   ├── models.py                # All database models (9 models)
│   ├── auth/                    # Authentication module
│   │   ├── routes.py            # Login, Register, Logout, Change Password
│   │   └── forms.py             # WTForms definitions
│   ├── admin/                   # Admin panel module
│   │   └── routes.py            # All admin operations (17 routes)
│   ├── quiz/                    # Quiz module
│   │   └── routes.py            # Quiz play, results, leaderboard, performance (10 routes)
│   ├── competition/             # Multiplayer competition module
│   │   └── routes.py            # Create, join, take, submit competition (9 routes)
│   ├── templates/
│   │   ├── base.html            # Master layout template
│   │   ├── home.html            # Landing page
│   │   ├── auth/                # Login, register, profile, change_password pages
│   │   ├── admin/               # 12 admin dashboard pages
│   │   ├── quiz/                # 9 quiz pages
│   │   └── competition/         # Competition pages
│   └── static/                  # CSS, JS, Images
├── migrations/                  # Database migration files
├── config.py                    # App configuration
├── main.py                      # App entry point
├── create_db.py                 # DB initialization + seed data
├── change_admin_password.py     # Admin password reset utility
├── requirements.txt             # Python dependencies
├── Procfile                     # Render deployment: gunicorn main:app
└── Dockerfile                   # Docker support
```

---

## Database Models

### 1. User Model
Fields: `id, username (unique), email, password_hash, role (user/admin)`
Methods: `set_password(), check_password(), is_admin()`
Relationships: attempts, leaderboard_entries, feedbacks, competitions_created, competition_attempts

### 2. Category Model
Fields: `id, name (unique)`
Relationships: questions, competitions

### 3. Question Model
Fields: `id, text, option1, option2, option3, option4, correct_option (1-4), explanation, category_id, difficulty (Easy/Medium/Hard)`

### 4. Attempt Model
Fields: `id, user_id, score, total, points, category_id, difficulty, created_at`
Points System: Easy = 2pts/question, Medium = 4pts/question, Hard = 6pts/question

### 5. AttemptAnswer Model
Fields: `id, attempt_id, question_id, chosen_option (1-4), correct (bool)`

### 6. LeaderboardEntry Model
Fields: `id, user_id, username, score, total, points, category_id, difficulty, created_at`

### 7. Feedback Model
Fields: `id, user_id, name, rating (1-5 stars), feedback_text, created_at`

### 8. Competition Model
Fields: `id, code (8-char unique), creator_id, category_id, difficulty, num_questions (default=10), time_limit (default=600s), status (waiting/in_progress/completed), created_at, started_at, ended_at, winner_id`

### 9. CompetitionAttempt Model
Fields: `id, competition_id, user_id, score (%), correct_answers, total_questions, time_taken, status (in_progress/completed), started_at, completed_at, answers (JSON)`

---

## All Features & Functions

### Authentication Module (/auth/)

| Function | Description |
|---|---|
| `register()` | Naya user account banao, username unique check karo |
| `login()` | Normal user login — admin ko yahan block kiya gaya hai |
| `admin_login()` | Sirf admin users ke liye alag login page |
| `logout()` | Session clear karo |
| `profile()` | Logged-in user ka profile page |
| `change_password()` | User apna password change kare |
| Legacy Password Support | Purane plain-text passwords ko auto hash mein upgrade |

---

### Quiz Module (/quiz/)

| Function | Route | Description |
|---|---|---|
| `select()` | /quiz/select | Category choose karo |
| `start()` | /quiz/start/category_id | Difficulty select karo |
| `start_quiz()` | /quiz/start/cat_id/difficulty | Quiz session shuru karo |
| `question()` | /quiz/question/q_id | Question dikhao, answer save karo |
| `result()` | /quiz/result | Score, points, answer review dikhao |
| `leaderboard()` | /quiz/leaderboard | Top 50 users ka ranking |
| `leaderboard_category()` | /quiz/leaderboard/category | Category-wise leaderboard |
| `api_leaderboard()` | /quiz/api/leaderboard | JSON API for leaderboard |
| `performance_dashboard()` | /quiz/performance | User ka detailed analytics |
| `feedback()` | /quiz/feedback | Feedback form submit karo |

**Quiz Session Flow:**
1. Category select → Difficulty select → Max 10 questions load
2. 10-minute timer shuru (600 seconds)
3. Navigate: Previous / Next / Submit button
4. Auto-submit when time expires
5. Score calculate → Attempt save → LeaderboardEntry save → Result page

**Scoring:**
- Easy: 2 points per correct answer (max 20 points)
- Medium: 4 points per correct answer (max 40 points)
- Hard: 6 points per correct answer (max 60 points)

---

### Leaderboard System

- Filters: Today / This Week / This Month / All Time
- Category Filter: Kisi bhi category ke hisaab se filter karo
- Ordering: Points (desc), Score (desc), Date (desc)
- Shows Top 50 entries

---

### Performance Dashboard (/quiz/performance)

| Metric | Description |
|---|---|
| Total Quizzes Played | Kitne quiz khele |
| Average Score % | Overall percentage |
| Total Points Earned | Saare attempts ke total points |
| Score Over Time | Line chart — progress track karo |
| Points Over Time | Chart — points trend |
| Competition Stats | Competition attempts ka summary |

Admin can view any user's performance by passing user_id param.

---

### Competition Module (/competition/)

| Function | Route | Description |
|---|---|---|
| `competition_menu()` | /competition/ | User ke active/completed competitions |
| `create_competition()` | /competition/create | Naya competition banao |
| `join_competition()` | /competition/join | 8-char code se join karo |
| `wait_for_opponent()` | /competition/wait/code | Opponent ka wait karo |
| `start_competition()` | /competition/start/code | Creator start kare (POST) |
| `take_competition_test()` | /competition/take/code | Quiz questions answer karo |
| `submit_answer()` | /competition/submit-answer/code | AJAX answer save (real-time) |
| `submit_competition_test()` | /competition/submit/code | Final submit |
| `competition_results()` | /competition/results/code | Results + answer review |

**Competition Flow:**
1. Creator selects Category + Difficulty + No. of Questions + Time Limit
2. Unique 8-char code generate hota hai
3. Creator waiting room mein hai, code share karta hai
4. Opponent code enter karke join karta hai
5. Creator "Start" button click karta hai → Both players start simultaneously
6. Same questions, same timer for both players
7. Auto-submit on time expiry
8. Higher score wala winner
9. Detailed answer review for both players

**Competition Rules:**
- Max 2 players only
- Creator cannot join own competition
- Stale competitions (waiting > 3 min) auto-delete
- Minimum 2 players required to start

---

### Admin Panel (/admin/)

| Function | Route | Description |
|---|---|---|
| `index()` | /admin/ | Dashboard — all categories + questions |
| `categories()` | /admin/categories | Categories add/manage |
| `new_question()` | /admin/question/new | Add single question |
| `edit_question()` | /admin/question/edit/id | Edit existing question |
| `delete_question()` | /admin/question/delete/id | Delete question |
| `bulk_add_questions()` | /admin/questions/bulk-add | Add multiple questions at once |
| `users()` | /admin/users | All users list |
| `new_user()` | /admin/user/new | Create new user |
| `edit_user()` | /admin/user/edit/id | Edit user details |
| `delete_user()` | /admin/user/delete/id | Delete user |
| `change_user_password()` | /admin/user/change-password/id | Reset any user's password |
| `competitions_view()` | /admin/competitions | All completed competitions |
| `feedback()` | /admin/feedback | View user feedbacks |
| `user_progress()` | /admin/user-progress | Platform-wide analytics |
| `user_progress_detail()` | /admin/user/id/progress | Single user detail analytics |
| `admin_user_performance()` | /admin/user/id/performance | User performance dashboard |
| `admin_profile()` | /admin/profile | Admin profile |

---

## URL Routes — Complete List

```
/                                    Home page

# Auth
/auth/register                       User registration
/auth/login                          User login
/auth/admin/login                    Admin login (separate page)
/auth/logout                         Logout
/auth/profile                        User profile
/auth/change-password                Change own password

# Quiz
/quiz/select                         Category selection
/quiz/start/<category_id>            Difficulty selection
/quiz/start/<cat_id>/<difficulty>    Start quiz session
/quiz/question/<q_id>                Quiz question page
/quiz/result                         Quiz result page
/quiz/leaderboard                    Main leaderboard
/quiz/leaderboard/<category_name>    Category leaderboard
/quiz/api/leaderboard                JSON API endpoint
/quiz/performance                    Performance dashboard
/quiz/feedback                       Feedback form

# Competition
/competition/                        Competition hub
/competition/create                  Create competition
/competition/join                    Join with code
/competition/wait/<code>             Waiting room
/competition/start/<code>            Start (POST, creator only)
/competition/take/<code>             Take quiz
/competition/submit-answer/<code>    Save answer AJAX (POST)
/competition/submit/<code>           Final submit (POST)
/competition/results/<code>          Results page

# Admin (all require admin login)
/admin/                              Admin dashboard
/admin/categories                    Manage categories
/admin/question/new                  Add question
/admin/question/edit/<id>            Edit question
/admin/question/delete/<id>          Delete question
/admin/questions/bulk-add            Bulk add questions
/admin/users                         User management
/admin/user/new                      Create user
/admin/user/edit/<id>                Edit user
/admin/user/delete/<id>              Delete user
/admin/user/change-password/<id>     Change user password
/admin/competitions                  View competitions
/admin/feedback                      View feedback
/admin/user-progress                 Analytics dashboard
/admin/user/<id>/progress            User detail analytics
/admin/user/<id>/performance         User performance
/admin/profile                       Admin profile
```

---

## User Flow (Normal User)

```
1. Visit Homepage (/)
2. Register → /auth/register
3. Login → /auth/login
4. Select Category → /quiz/select
5. Select Difficulty → Easy / Medium / Hard
6. Start Quiz → 10 questions, 10-minute timer
7. Answer Questions → Navigate prev/next
8. Submit / Auto-submit on time expiry
9. View Results → Score, Points, Answer Review with explanations
10. View Leaderboard → /quiz/leaderboard
11. View Performance → /quiz/performance
12. Join or Create Competition → /competition/
13. Submit Feedback → /quiz/feedback
```

---

## Security Features

| Feature | Implementation |
|---|---|
| Password Hashing | PBKDF2-SHA256 (Werkzeug), 150,000 iterations |
| CSRF Protection | Flask-WTF on all forms |
| Session Management | Flask-Login |
| Role-Based Access | admin_required decorator on all admin routes |
| Admin Separation | Alag admin login page, regular login pe admin block |
| Self-Delete Prevention | Admin apna account delete nahi kar sakta |
| Legacy Password Upgrade | Plain-text passwords auto hash mein convert |

---

## Issues & Bugs Found

### CRITICAL Issues

| # | Issue | Location | Status |
|---|---|---|---|
| 1 | No email verification | Register page | ⏳ Pending |
| 2 | No rate limiting | Login, Register | ✅ **FIXED Oct 25** — Flask-Limiter added |
| 3 | No forgot password feature | Auth module | ✅ **FIXED Oct 25** — Full flow added |
| 4 | DEBUG print statements in production | competition/routes.py | ⏳ Pending |
| 5 | No input sanitization on questions | Admin question form | ⏳ Pending |

### MODERATE Issues

| # | Issue | Location | Status |
|---|---|---|---|
| 6 | Computer category incomplete | Database | ✅ **FIXED Oct 25** — 20 questions added |
| 7 | Questions never randomize | Quiz engine | ✅ **FIXED Oct 25** — random.shuffle() added |
| 8 | No pagination | Leaderboard, User list | ⏳ Pending |
| 9 | Email field optional on register | Register form | ⏳ Pending |
| 10 | Competition only 2 players | Competition module | ⏳ Pending |
| 11 | Leaderboard has duplicate entries | LeaderboardEntry model | ✅ **FIXED Oct 25** — Best score per user |
| 12 | No quiz question randomization | Quiz engine | ✅ **FIXED Oct 25** — Same as #7 |

### MINOR Issues

| # | Issue | Status |
|---|---|---|
| 13 | Admin cannot play quizzes | ⏳ Pending |
| 14 | No dark/light mode toggle | ⏳ Pending |
| 15 | No mobile-optimized UI | ⏳ Pending |
| 16 | No loading states in competition | ⏳ Pending |

---

## Industry-Level Improvements Needed

### Priority 1 — Security (Must Fix First)

```
1. Forgot Password / Password Reset via Email
   → Flask-Mail + token-based reset link (itsdangerous)

2. Rate Limiting on Login/Register
   → Flask-Limiter: max 5 login attempts/minute

3. Email Verification on Registration
   → Send verification link before account activation

4. Remove all DEBUG print() statements
   → Use Python logging module (logging.info, logging.debug)

5. Input Sanitization for question text
   → Use bleach library to prevent XSS
```

### Priority 2 — User Experience

```
6. Complete "Computer" category
   → Add 10 Medium + 10 Hard questions

7. Question Randomization
   → import random; random.shuffle(questions)

8. Profile Page Enhancement
   → Show total quizzes, avg score, badges, recent history

9. Social Result Sharing
   → "Share on WhatsApp/Twitter" button on result page

10. Quiz Review Improvement
    → Better card-style UI with color-coded correct/wrong

11. Mobile Responsive Design
    → Test and fix Bootstrap grid for small screens

12. Custom Error Pages
    → 404, 403, 500 custom pages with navigation
```

### Priority 3 — New Features

```
13. Guest Quiz Mode (without login)
    → Try 5 questions as guest, then prompt to register

14. Practice Mode
    → No timer, unlimited questions, instant feedback

15. Badge/Achievement System
    → "First Quiz", "Perfect Score", "5-Day Streak" badges

16. Profile Avatars
    → Gravatar integration based on email

17. Email Notifications
    → Competition invite, result summary emails

18. Leaderboard Fix — Best Score Only
    → Show only best attempt per user per category

19. CSV Question Import for Admin
    → Upload spreadsheet to bulk add questions

20. Competition Invite via Link
    → quizcraft.com/join/ABCD1234 shareable link
```

### Priority 4 — Performance & Scalability

```
21. Caching for Leaderboard
    → Flask-Caching: cache leaderboard for 5 minutes

22. Pagination
    → Leaderboard (20/page), User List (25/page), Questions (30/page)

23. Real-time Competition
    → Flask-SocketIO for live progress updates

24. Logging System
    → Replace all print() with Python logging

25. Environment Variables
    → Use python-dotenv for all secrets

26. Database Connection Pooling
    → SQLAlchemy pool_size=10 for production

27. API Rate Limiting
    → /api/leaderboard max 30 requests/minute
```

---

## Priority Action Plan

### Phase 1 — Critical Fixes ✅ COMPLETED Oct 25
1. ✅ Rate limiting on login/register/forgot-password — Flask-Limiter
2. ✅ Forgot password + email reset — full token-based flow
3. ✅ Computer category completed — 10 Medium + 10 Hard questions added
4. ✅ Question randomization — random.shuffle() on every quiz start
5. ✅ Leaderboard best-score fix — one entry per user per category
6. ⏳ Remove all `print()` debug statements from competition/routes.py

### Phase 2 — UX Improvements
7. ✅ **DONE Oct 25** — Remove debug `print()` statements → proper `logging` module
8. ✅ **DONE Oct 25** — Custom 404/403/500 error pages
9. ⏳ Mobile responsive audit and fixes
10. ⏳ Profile page with stats + recent quiz history

### Phase 3 — New Features
11. ⏳ Guest quiz mode (5 questions without login)
12. ⏳ Badge/achievement system
13. ⏳ CSV question import for admin
14. ⏳ Social share result button
15. ⏳ Email notifications for competition invites

### Phase 4 — Scale for Real Users
16. ⏳ Real-time competition via WebSockets (Flask-SocketIO)
17. ⏳ Caching for leaderboard (Flask-Caching)
18. ⏳ Pagination for all list views
19. ⏳ Email verification for new registrations
20. ⏳ Admin analytics enhancement with charts

---

## Admin Credentials

| Field | Value |
|---|---|
| Admin Login URL | /auth/admin/login |
| Username | omyadav |
| Password | Admin@123 (recently reset) |

---

## How to Run Locally

```bash
# 1. Enter directory
cd "QUIZ CRAFT Project/QuizCraft"

# 2. Activate virtual environment (Windows)
venv311\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python create_db.py

# 5. Run development server
python main.py

# Visit: http://127.0.0.1:5000
```

## Production Deployment (Render)

- **Procfile:** `web: gunicorn main:app`
- **Build Command:** `python create_db.py`
- **Environment Variables needed:**
  - `DATABASE_URL` — PostgreSQL connection string
  - `SECRET_KEY` — Flask secret key

---

---

## Changelog

### October 26, 2026
| # | Change | File(s) Modified |
|---|---|---|
| 23 | **Brevo REST API Mailer** — Replaced blocked Render SMTP with Brevo HTTPS REST API | `config.py`, `app/auth/routes.py`, `requirements.txt` |
| 24 | **Disposable Email Blocklist** — Blocked disposable/temporary domains at registration | `app/auth/routes.py` |
| 25 | **User Model Verification Fields** — Added `is_verified`, `verified_at`, `google_id`, made `password_hash` nullable | `app/models.py` |
| 26 | **Email Verification & Resend Routes** — Added `/auth/verify-email/<token>` and `/auth/resend-verification` | `app/auth/routes.py`, `app/templates/auth/resend_verification.html` |
| 27 | **Unverified Login Guard** — Blocks unverified users on login with spam folder notice and resend link | `app/auth/routes.py`, `app/templates/auth/login.html` |
| 28 | **Supabase Phase 1 Migration** — Safe PostgreSQL migration script created with omyadav verification | `phase1_email_verification_supabase.sql` |
| 17 | **Admin Forgot Password** — Added 'Forgot Password?' link on Admin Login page | `app/templates/auth/admin_login.html` |
| 18 | **Admin Password Reset Redirection** — Redirects admin users directly to Admin Login after reset | `app/auth/routes.py` |
| 19 | **Unified Auth Navigation** — Added quick switch between User Login & Admin Login | `app/templates/auth/forgot_password.html`, `app/templates/auth/reset_password.html` |
| 20 | **Supabase Production DB Update** — 20 Computer questions (Medium+Hard) inserted directly into Supabase (Total 300) | Supabase PostgreSQL |
| 21 | **Admin Email Sanitized** — Removed trailing 'None' artifact from admin email in Supabase & local DB | Supabase & SQLite |
| 22 | **Docker Python 3.10 Build Fix** — Pinned SQLAlchemy==2.0.38 and wrapt==1.17.2, removed BOM | `requirements.txt` |

### October 25, 2026 — Part 2
| # | Change | File(s) Modified |
|---|---|---|
| 11 | **Debug Print Removal** — All `print()` replaced with `logging.getLogger()` | `app/competition/routes.py`, `app/quiz/routes.py`, `app/auth/routes.py` |
| 12 | **Custom 404 Page** — Friendly "Page Not Found" template | `app/templates/404.html` |
| 13 | **Custom 403 Page** — Friendly "Access Denied" template | `app/templates/403.html` |
| 14 | **Custom 500 Page** — Friendly "Server Error" template | `app/templates/500.html` |
| 15 | **Error Handlers Registered** — 404/403/500 handlers added to app factory | `app/__init__.py` |
| 16 | **Supabase SQL Script** — Computer category questions SQL for production DB | `computer_questions_supabase.sql` |
|---|---|---|
| 1 | **Question Shuffle** — `random.shuffle()` added before quiz starts | `app/quiz/routes.py` |
| 2 | **Leaderboard Fix** — Best score per user per category (no duplicates) | `app/quiz/routes.py` |
| 3 | **Rate Limiting** — Flask-Limiter on login (5/min), register (10/min), forgot-password (3/min) | `app/__init__.py`, `app/auth/routes.py` |
| 4 | **Forgot Password** — Full token-based email reset flow (30 min expiry) | `app/auth/routes.py`, `app/auth/forms.py`, new templates |
| 5 | **forgot_password.html** — New template for forgot password form | `app/templates/auth/forgot_password.html` |
| 6 | **reset_password.html** — New template for password reset via token | `app/templates/auth/reset_password.html` |
| 7 | **Login page** — "Forgot Password?" link added | `app/templates/auth/login.html` |
| 8 | **Mail Config** — Flask-Mail SMTP settings via env vars | `config.py` |
| 9 | **Computer Category** — 10 Medium + 10 Hard questions added (total 300 now) | Database (local + needs Supabase SQL) |
| 10 | **Packages Updated** — flask-limiter, flask-mail, flask-sqlalchemy 3.x, sqlalchemy 2.x | `requirements.txt` |

---

*Last Updated: October 26, 2026 | Auto-maintained by Antigravity IDE*
