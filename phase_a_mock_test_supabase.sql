-- ==============================================================================
-- QuizCraft: Phase A - Placement Mock Test Engine Migration
-- Safe & Idempotent SQL script for Supabase PostgreSQL
-- ==============================================================================

-- 1. Mock Test Table (Company Name, Title, Duration, Attempt Rules)
CREATE TABLE IF NOT EXISTS mock_test (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    allow_multiple_attempts BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_mock_test_company ON mock_test(company_name);
CREATE INDEX IF NOT EXISTS idx_mock_test_active ON mock_test(is_active);

-- 2. Mock Section Table (Numerical Ability, Verbal Ability, Reasoning, etc.)
CREATE TABLE IF NOT EXISTS mock_section (
    id SERIAL PRIMARY KEY,
    test_id INTEGER NOT NULL REFERENCES mock_test(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 1,
    num_questions INTEGER NOT NULL DEFAULT 10,
    section_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_mock_section_test_id ON mock_section(test_id);

-- 3. Mock Question Table
CREATE TABLE IF NOT EXISTS mock_question (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES mock_section(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_option INTEGER NOT NULL,
    explanation TEXT,
    marks INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_mock_question_section_id ON mock_question(section_id);

-- 4. Mock Attempt Table (Server Deadline, Violations, Status, Question Order Shuffle)
CREATE TABLE IF NOT EXISTS mock_attempt (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    test_id INTEGER NOT NULL REFERENCES mock_test(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    server_deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(30) NOT NULL DEFAULT 'in_progress',
    score INTEGER NOT NULL DEFAULT 0,
    total_marks INTEGER NOT NULL DEFAULT 0,
    violation_count INTEGER NOT NULL DEFAULT 0,
    question_order JSONB
);

CREATE INDEX IF NOT EXISTS idx_mock_attempt_user ON mock_attempt(user_id);
CREATE INDEX IF NOT EXISTS idx_mock_attempt_test ON mock_attempt(test_id);
CREATE INDEX IF NOT EXISTS idx_mock_attempt_status ON mock_attempt(status);

-- 5. Mock Answer Table (Autosaved Student Selections, Review Flag, Time Spent)
CREATE TABLE IF NOT EXISTS mock_answer (
    id SERIAL PRIMARY KEY,
    attempt_id INTEGER NOT NULL REFERENCES mock_attempt(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES mock_question(id) ON DELETE CASCADE,
    chosen_option INTEGER,
    marked_for_review BOOLEAN NOT NULL DEFAULT FALSE,
    time_spent INTEGER NOT NULL DEFAULT 0,
    is_correct BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_mock_answer_attempt ON mock_answer(attempt_id);
CREATE INDEX IF NOT EXISTS idx_mock_answer_question ON mock_answer(question_id);

-- 6. Mock Violation Table (Anti-Cheat Discipline Logging)
CREATE TABLE IF NOT EXISTS mock_violation (
    id SERIAL PRIMARY KEY,
    attempt_id INTEGER NOT NULL REFERENCES mock_attempt(id) ON DELETE CASCADE,
    violation_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_mock_violation_attempt ON mock_violation(attempt_id);
