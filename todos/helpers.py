import sqlite3

def add_todo(owner_id, assign_to_id, description):
    print("unsafe function running!")
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    script = f"INSERT INTO todos_todo (description, done, assigned_to_id, owner_id) VALUES ('{description}', False, {assign_to_id}, {owner_id});"
    cursor.executescript(script)
    conn.commit()
