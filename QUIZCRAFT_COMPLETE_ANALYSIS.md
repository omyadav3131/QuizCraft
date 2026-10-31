# QuizCraft — Complete Project Analysis & Documentation

> **Live URL:** [https://quizcraft-qt15.onrender.com](https://quizcraft-qt15.onrender.com)
> **Author:** Om Yadav | **GitHub:** [omyadav3131](https://github.com/omyadav3131)
> **Status:** Deployed & Live on Render
> **Last Updated:** October 30, 2026

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

### 10. MockTest Model (Placement Mocks)
Fields: `id, company_name, title, description, duration_minutes, is_active, allow_multiple_attempts, created_at`
Relationships: `sections` (cascade delete), `attempts`

### 11. MockSection Model
Fields: `id, test_id, name, order, num_questions, section_minutes, created_at`
Relationships: `test`, `questions` (cascade delete)

### 12. MockQuestion Model
Fields: `id, section_id, text, option1, option2, option3, option4, correct_option (1-4), explanation, marks, created_at`
Relationships: `section`

### 13. MockAttempt Model
Fields: `id, user_id, test_id, started_at, server_deadline, submitted_at, status ('in_progress','completed','timed_out','disqualified'), score, total_marks, violation_count, question_order (JSON)`
Relationships: `user`, `test`, `answers` (cascade delete), `violations` (cascade delete)

### 14. MockAnswer Model
Fields: `id, attempt_id, question_id, chosen_option (1-4 or None), marked_for_review (bool), time_spent (seconds), is_correct (bool)`
Relationships: `attempt`, `question`

### 15. MockViolation Model (Anti-Cheat Discipline)
Fields: `id, attempt_id, violation_type ('tab_switch','window_blur','fullscreen_exit'), timestamp`
Relationships: `attempt`

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

### Placement Mock Test Module (/mock/) — (New)

TCS NQT style real exam simulation with server-side timer, per-student question and option randomization, background autosave, and practice-mode anti-cheat discipline.

| Function | Route | Description |
|---|---|---|
| `test_list()` | /mock/ or /mock/tests | Company-wise placement mocks list |
| `instructions()` | /mock/test/\<id\>/instructions | Section breakdown, rules & mandatory checkbox |
| `start_test()` | /mock/test/\<id\>/start | Shuffles questions/options, sets server deadline, begins attempt |
| `take_test()` | /mock/attempt/\<id\> | TCS NQT exam interface with question palette & tabs |
| `save_answer()` | /mock/attempt/\<id\>/save | AJAX autosave on every selection with server clock sync |
| `record_violation()` | /mock/attempt/\<id\>/violation | Anti-cheat discipline event tracking (tab-switch/blur/fullscreen exit) |
| `submit_test()` | /mock/attempt/\<id\>/submit | Final submission with zero negative marking |
| `result()` | /mock/attempt/\<id\>/result | Scorecard, section-wise accuracy, time spent & solutions review |

**Mock Test Exam Engine Highlights:**
1. **Strict Zero Negative Marking:** Correct = +1 mark (or question weight), wrong or unattempted = 0 marks.
2. **Server-Side Deadline:** `server_deadline = started_at + duration_minutes`. Client clock drift has no effect; auto-submits on expiration.
3. **Deterministic Per-Student Randomization:** Randomizes questions and option sequence per candidate upon test start, persisted in `attempt.question_order` (JSON). Reopening/refreshing guarantees the exact same order.
4. **TCS-Style Palette:** Answered (Green), Not Answered (Red), Not Visited (Grey), Marked for Review (Purple), Answered & Marked for Review (Purple + Green dot).
5. **Begin Exam Blocking Overlay (Fullscreen Gesture Compliance):**
   - Modern browsers block programmatic `requestFullscreen()` unless triggered by a direct user gesture (click).
   - Exam loads with a blocking `#beginExamOverlay` concealing questions.
   - Clicking **"Begin Exam"** requests fullscreen mode, sets `hasExamStarted = true`, and reveals the test.
   - Unsupported devices/browsers receive a fallback notice and continue normally.
   - Anti-cheat tracking does NOT record violations until after the candidate clicks "Begin Exam".
6. **All Questions Mandatory Rule:**
   - **Client-Side:** The "Submit Test" button remains disabled until every question has a chosen option (`s.chosen_option !== null`). Questions marked for review without choosing an option remain count-blocked. A dynamic badge indicates `Answer all questions (N left)`.
   - **Server-Side:** Manual submission (`POST /mock/attempt/<id>/submit`) strictly validates that `answered_count == total_questions`. If incomplete, the submission is rejected with a flash message and redirects back to the exam.
   - **Automatic Finalizations Unblocked:** Automatic submissions due to timer expiry (`timed_out`) and maximum violations (`disqualified`) bypass this requirement and submit immediately with partial answers.
7. **Score Calculation on Auto-Submit:**
   - Computed fairly from answers saved up to the moment of auto-submit: correct answers = points, unanswered = 0, no negative marking.
   - Clear, friendly notice banners on result page: `"Auto-submitted when time ended"` and `"Auto-submitted due to 3 discipline violations"`.
8. **Anti-Cheat Controls & Honest Limitations:**
   - Focus loss and window blur detection via `visibilitychange` and `blur` events with a 1.2s client debounce.
   - Server-side 1.0s debounce to eliminate duplicate reporting between simultaneous browser focus events.
   - 3rd violation triggers instant auto-submission with `disqualified` status.
   - Prevented text copy, cut, paste, right-click, selection, and dev shortcut keys (F12, Ctrl+Shift+I/J/C, Ctrl+C/V/X/U/S/P).
   - Window `beforeunload` warning modal against accidental tab closure.
   - **Honest Limitations:** Best-effort browser-level discipline proctoring for recruitment simulations. It cannot detect external physical devices (smartphones, cameras), dual monitors without window focus change, or virtual machines without a native OS background daemon.
9. **Admin Helpers:**
   - **Reset Attempt:** Dedicated attempts management view (`/admin/mock-tests/<test_id>/attempts`) with a confirmation modal allowing an admin to delete a student's attempt, answers, and violation logs so they can retake the test.
   - **Multiple Attempts Toggle:** Configurable per test in the admin create/edit form (`allow_multiple_attempts`).

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
| `mock_tests_list()` | /admin/mock-tests | Placement mock tests management list |
| `mock_test_new()` | /admin/mock-tests/new | Create new company mock test |
| `mock_test_edit()` | /admin/mock-tests/\<id\>/edit | Edit mock test metadata & attempt rules |
| `mock_test_delete()` | /admin/mock-tests/\<id\>/delete | Delete mock test and cascade delete sections |
| `mock_sections_manage()` | /admin/mock-tests/\<id\>/sections | Manage sections & section order/time limits |
| `mock_questions_list()` | /admin/mock-tests/sections/\<sec_id\>/questions | View and filter questions in a section |
| `mock_question_new()` | /admin/mock-tests/sections/\<sec_id\>/questions/new | Add single question to section |
| `mock_question_edit()` | /admin/mock-tests/sections/\<sec_id\>/questions/\<q_id\>/edit | Edit section question |
| `mock_question_delete()` | /admin/mock-tests/sections/\<sec_id\>/questions/\<q_id\>/delete | Delete question from section |
| `mock_questions_bulk_add()` | /admin/mock-tests/sections/\<sec_id\>/bulk-add | Bulk add questions to mock section |
| `mock_test_attempts()` | /admin/mock-tests/\<test_id\>/attempts | View all candidate attempts and scores |
| `mock_attempt_reset()` | /admin/mock-attempts/\<attempt_id\>/reset | Reset candidate attempt to allow exam retake |

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

### Phase 2 — UX Improvements & Platform Standardization ✅ COMPLETED Oct 25-30
7. ✅ **DONE** — Remove debug `print()` statements → proper `logging` module
8. ✅ **DONE** — Custom 404/403/500 error pages
9. ✅ **DONE** — Mobile responsive audit and fixes across all screens (360px - 1440px)
10. ✅ **DONE** — User profile page with stats + quiz and mock test history
11. ✅ **DONE** — Standardized admin UI with breadcrumbs, instant search filters, and empty states
12. ✅ **DONE** — Admin navbar overflow and wrapping elimination on laptop screens (1366px)
13. ✅ **DONE** — IST (+5:30) timestamp display standardization across all user-facing views

### Phase 3 — Enterprise Placement Mock Engine ✅ COMPLETED Oct 26-30
14. ✅ **DONE** — Full-length Placement Mock Test engine (Phases A, B, C, D)
15. ✅ **DONE** — TCS NQT Pattern Diagnostic mock with 30 verified questions (Numerical, Verbal, Reasoning)
16. ✅ **DONE** — Practice-mode proctoring & anti-cheat discipline controls (fullscreen, focus loss, tab switch)
17. ✅ **DONE** — Anti-cheat concurrency race condition fix and post-finalization event rejection (HTTP 409)
18. ✅ **DONE** — Scannable post-submit result scorecard with interactive question filter chips
19. ✅ **DONE** — Strict Admin RBAC returning HTTP 403 Forbidden for non-admins across all admin actions

### Phase 4 — Authentication & Security Enhancements ✅ COMPLETED Oct 26
20. ✅ **DONE** — Brevo HTTPS REST API transactional emailer
21. ✅ **DONE** — Email verification token flow and unverified user login guard
22. ✅ **DONE** — Google OAuth 2.0 OpenID Connect sign-in with CSRF state protection

### Phase 5 — Future Roadmap & Remaining Backlog
23. ⏳ Real-time multiplayer competition upgrade to WebSockets (Flask-SocketIO)
24. ⏳ Caching for global leaderboard and category catalog (Flask-Caching / Redis)
25. ⏳ Server-side pagination for extensive question and user lists (>500 items)
26. ⏳ CSV/Excel bulk question import for admin
27. ⏳ Badge and achievement system for milestone test completions
28. ⏳ Social share card generator for exam scorecards

---

## Admin Credentials

| Field | Value |
|---|---|
| Admin Login URL | /auth/admin/login |
| Username | omyadav |
| Password | Managed securely in database (never stored in documentation) |

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
  - `BREVO_API_KEY` — Brevo v3 HTTPS REST API key for transactional emails
  - `MAIL_SENDER_EMAIL` — Verified sender email on Brevo
  - `GOOGLE_CLIENT_ID` — Google Cloud OAuth 2.0 Web Client ID
  - `GOOGLE_CLIENT_SECRET` — Google Cloud OAuth 2.0 Web Client Secret
  - `PREFERRED_URL_SCHEME` — `https` (handled automatically via ProxyFix)

---

---

## Changelog

### October 30, 2026 — Part 6 (Anti-Cheat Concurrency, Mock Result Redesign, Full Admin UI Polish & Student Experience)
| # | Change | File(s) Modified / Added |
|---|---|---|
| 58 | **Violation Concurrency & Race Condition Elimination (Phase 1a)** — In `/mock/attempt/<id>/violation`, added strict status validation rejecting non-in-progress attempts with HTTP 409 Conflict, stopping further events and redirecting client; capped timeline rows to `violation_count` | `app/mock/routes.py`, `app/templates/mock/exam.html`, `test_mock_engine.py` |
| 59 | **Doubled Apostrophes Sanitization (Phase 1b)** — Fixed literal doubled apostrophes in question text/options/explanations; created idempotent Supabase migration `fix_mock_apostrophes_supabase.sql` and verification script `scripts/check_apostrophes.py` asserting zero consecutive apostrophes | `scripts/seed_tcs_mock.py`, `seed_tcs_mock_supabase.sql`, `fix_mock_apostrophes_supabase.sql`, `scripts/check_apostrophes.py` |
| 60 | **IST Datetime Filter & Standardization (Phase 1c)** — Registered `@app.template_filter('to_ist')` converting UTC to IST (+5:30) with safe handling across naive and aware timestamps across mock results, user progress, competitions, feedback, and leaderboards | `app/__init__.py`, `app/mock/routes.py`, `app/templates/mock/result.html`, `app/templates/admin/*.html` |
| 61 | **Comprehensive Mock Result Scorecard Redesign (Phase 1d)** — Built scannable performance metrics (Score, Accuracy, Time, Violations), interactive question filters (All, Correct, Incorrect, Unanswered, Review), question jump palette, solution explanations, and proctoring audit log | `app/templates/mock/result.html` |
| 62 | **Admin Navbar Overflow & Wrapping Fix (Phase 2)** — Configured `flex-wrap: nowrap !important` on desktop with specialized breakpoint (`993px–1400px`) reducing link padding and font size; total width at 1366px is ~915px with ~450px breathing room and zero horizontal scroll | `app/static/css/professional.css`, `app/templates/base.html` |
| 63 | **Admin Mock Tests View Redesign (Phase 2)** — Standardized layout with Actions column (320px) always visible without horizontal scroll; responsive `.mock-test-card` for mobile screens; added instant search `#mockSearchInput` with counter; added `POST /admin/mock-tests/<id>/toggle-active` | `app/admin/routes.py`, `app/templates/admin/mock_tests.html`, `test_mock_engine.py` |
| 64 | **Platform-Wide Admin UI Standardization (Phase 2)** — Overhauled all 15 admin list and form views with breadcrumbs, empty-state notices, IST timestamps, delete confirmations, and instant client-side search across Categories, Questions, Users, Feedback, Progress, and Competitions | `app/templates/admin/*.html` |
| 65 | **Strict Admin RBAC 403 Enforcement (Phase 3)** — Updated `admin_required` decorator so authenticated non-admin users attempting to access or POST to admin endpoints receive HTTP 403 Forbidden (`abort(403)`), rendering `403.html`. Added unit test 25 | `app/admin/routes.py`, `test_mock_engine.py` |
| 66 | **Placement Mocks Catalog Grouping & Status (Phase 3)** — Grouped mock tests by company with clean responsive cards showing company chips, title, duration, question count, explicit Attempted / Not Attempted / In Progress badges, and clean empty state | `app/templates/mock/tests.html` |
| 67 | **Student Exam & Core Views Polish (Phase 3)** — Added mobile (<576px) and tablet (<768px) responsive rules to exam header, palette, actions toolbar, home page, category selection, difficulty selection, global leaderboard, and student profile; verified zero horizontal overflow at 375px | `app/templates/mock/exam.html`, `app/templates/mock/instructions.html`, `app/templates/home.html`, `app/templates/quiz/*.html`, `app/templates/auth/profile.html` |

### October 28, 2026 — Part 5 (PostgreSQL Timezone Compatibility & Render 500 Fix)
| # | Change | File(s) Modified / Added |
|---|---|---|
| 52 | **PostgreSQL Timezone Normalization** — Added `normalize_utc()` helper to ensure all `server_deadline` comparisons and subtractions work seamlessly across offset-aware PostgreSQL timestamps and naive datetimes without raising `TypeError` | `app/mock/routes.py` |
| 53 | **Safe Question Layout JSON Deserialization** — Added `get_sections_layout()` to safely parse JSON strings or dictionaries from `question_order` JSONB column on PostgreSQL without raising `AttributeError` | `app/mock/routes.py` |
| 54 | **Supabase Row Level Security (RLS) Explicit Disable** — Added explicit `ALTER TABLE mock_* DISABLE ROW LEVEL SECURITY` statements to `phase_a_mock_test_supabase.sql` so backend SQLAlchemy operations are never restricted | `phase_a_mock_test_supabase.sql` |
| 55 | **500 Error Logging** — Added `app.logger.error(..., exc_info=True)` to `@app.errorhandler(500)` so future internal server errors output the complete Python traceback to Render logs | `app/__init__.py` |
| 56 | **Silenced Relationship SAWarning** — Added `overlaps="attempts"` to `CompetitionAttempt.competition` relationship to eliminate warning output on startup | `app/models.py` |
| 57 | **Regression Test Suite Expansion** — Added test 23 in `test_mock_engine.py` explicitly asserting timezone-aware deadline comparisons, JSON string question layouts, and aware violation timestamps | `test_mock_engine.py` |

### October 27, 2026 — Part 4 (Mock Content Refinement & Production Deployment Readiness)
| # | Change | File(s) Modified / Added |
|---|---|---|
| 48 | **Mock Question Refinements** — Clarified Verbal Q11/Q12 target words ('TRANSPARENT', 'FRUGAL') without bold/underline markup; replaced debatable Q15 with unambiguous preposition question ('fond of') | `scripts/seed_tcs_mock.py`, `seed_tcs_mock_supabase.sql` |
| 49 | **Default Test Duration Adjusted** — Set default duration to 45 minutes (15 mins per section: Numerical, Verbal, Reasoning) while remaining editable via admin form | `scripts/seed_tcs_mock.py`, `seed_tcs_mock_supabase.sql` |
| 50 | **Self-Healing Supabase Production Migration Script** — Enhanced `seed_tcs_mock_supabase.sql` with zero-attempt purge/re-insert and attempt-preservation safety guard (logs NOTICE to edit via admin without mutating existing attempts) | `seed_tcs_mock_supabase.sql`, `scripts/generate_supabase_sql.py` |
| 51 | **Rigorous Independent Verification Suite** — Rewrote `scripts/verify_tcs_questions.py` with genuine formula derivations for all 16 computable questions and documented semantic rationales for 14 qualitative items | `scripts/verify_tcs_questions.py` |

### October 26, 2026 — Part 3 (Placement Mock Test Engine: Phases A, B, C, D)
| # | Change | File(s) Modified / Added |
|---|---|---|
| 39 | **Placement Mock Data Models (Phase A)** — Added `MockTest`, `MockSection`, `MockQuestion`, `MockAttempt`, `MockAnswer`, and `MockViolation` models | `app/models.py`, `phase_a_mock_test_supabase.sql` |
| 40 | **Server-Side Exam Engine & Shuffling (Phase A)** — Server-enforced countdown deadline, deterministic per-student question and option randomization, background autosave via AJAX, zero negative marking | `app/mock/routes.py`, `app/__init__.py` |
| 41 | **TCS NQT Style User Interface (Phase B)** — Instructions declaration gate, live color-coded question palette, section navigation tabs, mobile responsive floating palette drawer, and comprehensive post-submit result scorecard | `app/templates/mock/instructions.html`, `app/templates/mock/exam.html`, `app/templates/mock/result.html`, `app/templates/mock/tests.html` |
| 42 | **Practice Proctoring & Anti-Cheat Controls (Phase C)** — Fullscreen enforcement, focus loss & tab-switch detection (`visibilitychange`, `blur`), client & server debounce (1.0s), 3rd violation automatic submission/disqualification | `app/mock/routes.py`, `app/templates/mock/exam.html`, `app/templates/mock/result.html` |
| 43 | **Begin Exam User Gesture Fullscreen Compliance** — Added blocking `#beginExamOverlay` so `requestFullscreen()` is invoked strictly within a direct user click handler | `app/templates/mock/exam.html` |
| 44 | **Mandatory Answers Enforcement** — Submit Test button disabled until all questions are answered, live remaining count badge, server-side rejection of partial manual submissions (while timer expiry and 3rd violation auto-submit cleanly) | `app/templates/mock/exam.html`, `app/mock/routes.py` |
| 45 | **Admin Attempt Reset & Multiple Attempts Control** — Added dedicated attempt management view with confirm modal to reset/delete candidate attempts, plus per-test `allow_multiple_attempts` toggle | `app/admin/routes.py`, `app/templates/admin/mock_tests.html`, `app/templates/admin/mock_attempts.html` |
| 46 | **Sample Mock Content: TCS NQT Style Mock** — 30 original verified questions across Numerical Ability (10), Verbal Ability (10), and Reasoning Ability (10) with explanations and verification script | `scripts/verify_tcs_questions.py`, `scripts/seed_tcs_mock.py`, `seed_tcs_mock_supabase.sql` |
| 47 | **Comprehensive Test Suites** — 22 unit tests (`test_mock_engine.py`) and 12-check smoke test (`scripts/smoke_test_mock.py`) validating student flows, anti-cheat, secrecy, and reset attempt | `test_mock_engine.py`, `scripts/smoke_test_mock.py` |

### October 26, 2026 — Part 2 (Phase 2: Google OAuth 2.0)
| # | Change | File(s) Modified |
|---|---|---|
| 31 | **Google OAuth 2.0 Flow** — Lightweight OpenID Connect flow using `requests` (no heavy dependencies) | `config.py`, `app/auth/routes.py` |
| 32 | **OAuth CSRF State Protection** — Cryptographic random state stored in session and validated via `hmac.compare_digest` | `app/auth/routes.py` |
| 33 | **Account Linking & Duplicate Prevention** — Verified Google email automatically links `google_id` to existing account | `app/auth/routes.py` |
| 34 | **Admin Login Isolation** — Admin accounts blocked from Google OAuth sign-in to protect administrative integrity | `app/auth/routes.py` |
| 35 | **Google-Only Account Handling** — Friendly guidance on forgot password & change password for Google users | `app/auth/routes.py` |
| 36 | **Continue with Google Buttons** — Added official Google G SVG buttons to login and registration views | `app/templates/auth/login.html`, `app/templates/auth/register.html` |
| 37 | **Rate Limiting on OAuth** — 10 requests/minute on `/auth/google` and `/auth/google/callback` | `app/auth/routes.py` |
| 38 | **Security Sanitization** — Removed plain-text admin credentials from project documentation | `QUIZCRAFT_COMPLETE_ANALYSIS.md` |

### October 26, 2026 — Part 1 (Phase 1: Email Verification)
| # | Change | File(s) Modified |
|---|---|---|
| 23 | **Brevo REST API Mailer** — Replaced blocked Render SMTP with Brevo HTTPS REST API | `config.py`, `app/auth/routes.py`, `requirements.txt` |
| 24 | **Disposable Email Blocklist** — Blocked disposable/temporary domains at registration | `app/auth/routes.py` |
| 25 | **User Model Verification Fields** — Added `is_verified`, `verified_at`, `google_id`, made `password_hash` nullable | `app/models.py` |
| 26 | **Email Verification & Resend Routes** — Added `/auth/verify-email/<token>` and `/auth/resend-verification` | `app/auth/routes.py`, `app/templates/auth/resend_verification.html` |
| 27 | **Unverified Login Guard** — Blocks unverified users on login with spam folder notice and resend link | `app/auth/routes.py`, `app/templates/auth/login.html` |
| 28 | **Supabase Phase 1 Migration** — Safe PostgreSQL migration script created with omyadav verification | `phase1_email_verification_supabase.sql` |
| 29 | **Column Size Upgrades** — Expanded `password_hash` (255), `email` (255), `username` (150), `google_id` (255) | `app/models.py`, `app/auth/forms.py`, `phase1_email_verification_supabase.sql` |
| 30 | **Stacked Resend Rate Limiting** — 3 requests/min per IP and 1 request/min per (IP + email) | `app/auth/routes.py` |
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

*Last Updated: October 30, 2026 | Auto-maintained by Antigravity IDE*
