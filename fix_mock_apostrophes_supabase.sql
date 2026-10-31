-- ==============================================================================
-- fix_mock_apostrophes_supabase.sql
-- Idempotent script to fix doubled apostrophes in the mock_question table.
--
-- EXPLANATION:
-- In SQL string literals, two consecutive apostrophes ('') represent a single
-- literal apostrophe. If text was authored with SQL escaping and then saved
-- literally, two apostrophes ('') were stored in the database instead of one (').
--
-- In SQL literals:
--   '''''' (6 apostrophes) represents a string containing two apostrophes: ''
--   ''''   (4 apostrophes) represents a string containing one apostrophe: '
--
-- Calling REPLACE(col, '''''', '''') replaces every occurrence of '' with '
-- without affecting words that already have a single apostrophe.
-- This script is completely IDEMPOTENT: running it once cleans the data;
-- running it again finds 0 rows and makes no changes.
--
-- DO NOT RUN ANYWHERE UNTIL REVIEWED.
-- ==============================================================================

-- 1. PREVIEW: Count and list affected mock_question rows before the fix
SELECT
    id,
    section_id,
    CASE WHEN text LIKE '%''''%' THEN 'text ' ELSE '' END ||
    CASE WHEN option1 LIKE '%''''%' THEN 'option1 ' ELSE '' END ||
    CASE WHEN option2 LIKE '%''''%' THEN 'option2 ' ELSE '' END ||
    CASE WHEN option3 LIKE '%''''%' THEN 'option3 ' ELSE '' END ||
    CASE WHEN option4 LIKE '%''''%' THEN 'option4 ' ELSE '' END ||
    CASE WHEN explanation LIKE '%''''%' THEN 'explanation' ELSE '' END AS affected_columns,
    text
FROM mock_question
WHERE text LIKE '%''''%'
   OR option1 LIKE '%''''%'
   OR option2 LIKE '%''''%'
   OR option3 LIKE '%''''%'
   OR option4 LIKE '%''''%'
   OR explanation LIKE '%''''%';

-- 2. UPDATE: Replace doubled apostrophes ('') with a single apostrophe (')
-- Only updates rows that actually contain two consecutive apostrophes.
UPDATE mock_question
SET
    text = REPLACE(text, '''''', ''''),
    option1 = REPLACE(option1, '''''', ''''),
    option2 = REPLACE(option2, '''''', ''''),
    option3 = REPLACE(option3, '''''', ''''),
    option4 = REPLACE(option4, '''''', ''''),
    explanation = REPLACE(explanation, '''''', '''')
WHERE text LIKE '%''''%'
   OR option1 LIKE '%''''%'
   OR option2 LIKE '%''''%'
   OR option3 LIKE '%''''%'
   OR option4 LIKE '%''''%'
   OR explanation LIKE '%''''%';

-- 3. VERIFY: Confirm 0 rows remain with doubled apostrophes
SELECT COUNT(*) AS remaining_rows_with_doubled_apostrophes
FROM mock_question
WHERE text LIKE '%''''%'
   OR option1 LIKE '%''''%'
   OR option2 LIKE '%''''%'
   OR option3 LIKE '%''''%'
   OR option4 LIKE '%''''%'
   OR explanation LIKE '%''''%';

