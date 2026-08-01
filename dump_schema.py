import sqlite3

def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    with open('schema.txt', 'w', encoding='utf-8') as f:
        for table_name, sql in tables:
            f.write(f"--- TABLE: {table_name} ---\n")
            f.write(f"{sql}\n\n")
    conn.close()

if __name__ == '__main__':
    get_schema('quiz.db')
