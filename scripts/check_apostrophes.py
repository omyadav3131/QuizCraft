"""
Check for doubled apostrophes in seed_tcs_mock.py question data and seed_tcs_mock_supabase.sql.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from scripts.seed_tcs_mock import TCS_QUESTIONS_DATA

DOUBLE_APOS = "''"
found_py = []
for section, qs in TCS_QUESTIONS_DATA.items():
    for i, q in enumerate(qs, 1):
        for field in ['text', 'option1', 'option2', 'option3', 'option4', 'explanation']:
            v = q.get(field, '') or ''
            if DOUBLE_APOS in v:
                found_py.append((section, i, field, repr(v[:120])))

if found_py:
    print("DOUBLED APOSTROPHES IN seed_tcs_mock.py:")
    for f in found_py:
        print(f)
else:
    print("OK - No doubled apostrophes found in seed_tcs_mock.py")

# Also check seed_tcs_mock_supabase.sql for four consecutive apostrophes (which produce doubled apostrophes when run)
sql_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'seed_tcs_mock_supabase.sql'))
if os.path.exists(sql_path):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_lines = f.readlines()
    found_sql = []
    for line_num, line in enumerate(sql_lines, 1):
        if "''''" in line:
            found_sql.append((line_num, line.strip()))
    if found_sql:
        print("DOUBLED APOSTROPHES IN seed_tcs_mock_supabase.sql:")
        for line_num, line in found_sql:
            print(f"  Line {line_num}: {line[:120]}")
    else:
        print("OK - No four-apostrophes (doubled) found in seed_tcs_mock_supabase.sql")
