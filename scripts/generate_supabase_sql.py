"""
Generate idempotent and self-healing seed_tcs_mock_supabase.sql from TCS_QUESTIONS_DATA.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.seed_tcs_mock import TCS_QUESTIONS_DATA

def sql_escape(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

lines = []
lines.append("-- =====================================================================")
lines.append("-- FILE: seed_tcs_mock_supabase.sql")
lines.append("-- PURPOSE: Self-healing & idempotent SQL script to seed 'TCS NQT Style Mock'")
lines.append("--          on Supabase PostgreSQL.")
lines.append("-- BEHAVIOR ON RERUN:")
lines.append("--   - If 'TCS NQT Style Mock' does not exist, it creates the test, 3 sections,")
lines.append("--     and all 30 verified questions (45 mins total, 15 mins per section).")
lines.append("--   - If 'TCS NQT Style Mock' ALREADY exists and has 0 student attempts, it safely")
lines.append("--     purges any outdated sections and questions and re-inserts the clean,")
lines.append("--     mathematically verified question set. No duplicates, no orphan rows.")
lines.append("--   - If attempts exist, it does NOT modify questions at all to protect attempt")
lines.append("--     integrity, and instructs the administrator to edit via the admin panel.")
lines.append("-- USAGE INSTRUCTIONS:")
lines.append("--   1. Open the Supabase Dashboard -> SQL Editor.")
lines.append("--   2. Paste this entire file into the editor and click 'Run'.")
lines.append("-- =====================================================================\n")
lines.append("DO $$")
lines.append("DECLARE")
lines.append("    v_test_id INTEGER;")
lines.append("    v_attempt_count INTEGER := 0;")
lines.append("    v_sec_num_id INTEGER;")
lines.append("    v_sec_verb_id INTEGER;")
lines.append("    v_sec_reas_id INTEGER;")
lines.append("BEGIN")
lines.append("    -- 1. Check if 'TCS NQT Style Mock' Test exists")
lines.append("    SELECT id INTO v_test_id FROM mock_test WHERE title = 'TCS NQT Style Mock' AND company_name = 'TCS';")
lines.append("    ")
lines.append("    IF v_test_id IS NULL THEN")
lines.append("        INSERT INTO mock_test (company_name, title, description, duration_minutes, is_active, allow_multiple_attempts, created_at)")
lines.append("        VALUES (")
lines.append("            'TCS',")
lines.append("            'TCS NQT Style Mock',")
lines.append("            'Simulated TCS NQT placement examination featuring 3 core sections: Numerical Ability, Verbal Ability, and Reasoning Ability. Zero negative marking, single-attempt rule, and proctoring discipline monitoring.',")
lines.append("            45,")
lines.append("            TRUE,")
lines.append("            FALSE,")
lines.append("            NOW()")
lines.append("        ) RETURNING id INTO v_test_id;")
lines.append("        RAISE NOTICE 'Created test: TCS NQT Style Mock with ID %', v_test_id;")
lines.append("    ELSE")
lines.append("        SELECT COUNT(*) INTO v_attempt_count FROM mock_attempt WHERE test_id = v_test_id;")
lines.append("        IF v_attempt_count = 0 THEN")
lines.append("            RAISE NOTICE 'Found existing TCS NQT Style Mock (ID %) with 0 attempts. Purging outdated questions and sections for clean update...', v_test_id;")
lines.append("            DELETE FROM mock_question WHERE section_id IN (SELECT id FROM mock_section WHERE test_id = v_test_id);")
lines.append("            DELETE FROM mock_section WHERE test_id = v_test_id;")
lines.append("        ELSE")
lines.append("            RAISE NOTICE 'TCS NQT Style Mock (ID %) has % attempt(s). Existing sections and questions were NOT modified to preserve attempt history. Please edit questions via the QuizCraft Admin Panel.', v_test_id, v_attempt_count;")
lines.append("            RETURN;")
lines.append("        END IF;")
lines.append("    END IF;\n")
lines.append("    -- Update test metadata")
lines.append("    UPDATE mock_test")
lines.append("    SET description = 'Simulated TCS NQT placement examination featuring 3 core sections: Numerical Ability, Verbal Ability, and Reasoning Ability. Zero negative marking, single-attempt rule, and proctoring discipline monitoring.',")
lines.append("        duration_minutes = 45,")
lines.append("        is_active = TRUE,")
lines.append("        allow_multiple_attempts = FALSE")
lines.append("    WHERE id = v_test_id;\n")

sec_var_map = {
    'Numerical Ability': ('v_sec_num_id', 1),
    'Verbal Ability': ('v_sec_verb_id', 2),
    'Reasoning Ability': ('v_sec_reas_id', 3)
}

for sec_name, (var_name, order_idx) in sec_var_map.items():
    questions = TCS_QUESTIONS_DATA[sec_name]
    lines.append(f"    -- 2.{order_idx}. Section: {sec_name}")
    lines.append(f"    SELECT id INTO {var_name} FROM mock_section WHERE test_id = v_test_id AND name = '{sec_name}';")
    lines.append(f"    IF {var_name} IS NULL THEN")
    lines.append(f"        INSERT INTO mock_section (test_id, name, \"order\", num_questions, section_minutes, created_at)")
    lines.append(f"        VALUES (v_test_id, '{sec_name}', {order_idx}, {len(questions)}, 15, NOW())")
    lines.append(f"        RETURNING id INTO {var_name};")
    lines.append(f"        RAISE NOTICE 'Created section: {sec_name} with ID %', {var_name};")
    lines.append(f"    ELSE")
    lines.append(f"        UPDATE mock_section")
    lines.append(f"        SET \"order\" = {order_idx}, num_questions = {len(questions)}, section_minutes = 15")
    lines.append(f"        WHERE id = {var_name};")
    lines.append(f"        RAISE NOTICE 'Updated section: {sec_name} (ID %)', {var_name};")
    lines.append(f"    END IF;\n")

    for i, q in enumerate(questions, 1):
        q_text = sql_escape(q['text'])
        opt1 = sql_escape(q['option1'])
        opt2 = sql_escape(q['option2'])
        opt3 = sql_escape(q['option3'])
        opt4 = sql_escape(q['option4'])
        corr = q['correct_option']
        exp = sql_escape(q['explanation'])

        lines.append(f"    -- {sec_name} Question {i}")
        lines.append(f"    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)")
        lines.append(f"    VALUES ({var_name}, {q_text}, {opt1}, {opt2}, {opt3}, {opt4}, {corr}, {exp}, 1, NOW());\n")

lines.append("    RAISE NOTICE 'Successfully seeded all 30 questions for TCS NQT Style Mock.';")
lines.append("END $$;")

sql_content = '\n'.join(lines)
with open('seed_tcs_mock_supabase.sql', 'w', encoding='utf-8') as f:
    f.write(sql_content)

print(f"Generated seed_tcs_mock_supabase.sql successfully ({len(sql_content)} characters).")
