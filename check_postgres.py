import psycopg2
import sys

db_url = "postgresql://postgres.flfasaiwtiqtmvlrtwhg:%40Savitayadav3178@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"

try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("=== QUERY 1: All Tables in Public Schema ===")
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;")
    tables = cur.fetchall()
    for t in tables:
        print(t[0])
        
    print("\n=== QUERY 2: Total Number of Tables ===")
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")
    count = cur.fetchone()[0]
    print(count)
    
    print("\n=== QUERY 3: Tables named '%user%' ===")
    cur.execute("SELECT schemaname, tablename FROM pg_tables WHERE tablename ILIKE '%user%';")
    similar_users = cur.fetchall()
    for s in similar_users:
        print(s)
        
    has_user = any(t[0] == 'user' for t in tables)
    if has_user:
        print("\n=== QUERY 4: User Table Count ===")
        cur.execute('SELECT COUNT(*) FROM "user";')
        user_count = cur.fetchone()[0]
        print(user_count)
        
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
