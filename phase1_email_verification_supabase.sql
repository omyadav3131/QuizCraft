-- ====================================================================
-- QuizCraft Phase 1: Email Verification & Column Lengths Migration
-- Target: Supabase PostgreSQL Production Database
-- REMINDER: Please take a database backup in Supabase before executing.
-- ====================================================================

-- 1. Add new columns safely if they do not exist
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP NULL;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE NULL;

-- 2. Expand string column lengths to prevent truncation / value-too-long errors:
--    - password_hash: Werkzeug scrypt hashes are ~162 chars (VARCHAR 128 was too small)
--    - email: standard RFC 5321 emails can be up to 254 characters
--    - username: accommodates longer display names and matches leaderboard username (VARCHAR 150)
--    - google_id: accommodates standard OpenID Connect subject identifiers (VARCHAR 255)
ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(255);
ALTER TABLE "user" ALTER COLUMN email TYPE VARCHAR(255);
ALTER TABLE "user" ALTER COLUMN username TYPE VARCHAR(150);
ALTER TABLE "user" ALTER COLUMN google_id TYPE VARCHAR(255);

-- 3. Make password_hash nullable (so Google-authenticated users in Phase 2 won't require a password)
ALTER TABLE "user" ALTER COLUMN password_hash DROP NOT NULL;

-- 4. Mark ONLY 'omyadav' as verified; all other accounts remain unverified
UPDATE "user" SET is_verified = TRUE, verified_at = NOW() WHERE username = 'omyadav';
UPDATE "user" SET is_verified = FALSE WHERE username != 'omyadav';

-- 5. Verify the updated schema and records
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns 
WHERE table_name = 'user'
ORDER BY ordinal_position;

SELECT id, username, email, role, is_verified, verified_at FROM "user";
