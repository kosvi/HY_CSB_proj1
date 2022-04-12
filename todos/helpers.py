import sqlite3
from django.contrib.auth.models import User
from .models import Todo

# This function uses direct database queries instead of ORM
# And it seems the programmer has no clue what he/she is doing, since 
# the function actually uses "executescript" allowing all kinds of sql-injections!
def add_todo(owner_id, assign_to_id, description):
    print("unsafe function running!")
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    script = f"INSERT INTO todos_todo (description, done, assigned_to_id, owner_id) VALUES ('{description}', False, {assign_to_id}, {owner_id});"
    cursor.executescript(script)
    conn.commit()


# Functions below are used to reset the database

def remove_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auth_user WHERE 1=1;")
    conn.commit()

def remove_all_todos(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos_todo WHERE 1=1;")
    conn.commit()

def add_user_after_reset(username, password, email, is_admin = False):
    user = User.objects.create_user(username=username, password=password, email=email)
    if is_admin:
        user.is_staff = True
        user.is_admin = True
    user.save()
    return user

def add_todo_after_reset(owner, assigned_to, description, done = False):
    todo = Todo()
    todo.owner = owner
    todo.assigned_to = assigned_to
    todo.description = description
    todo.done = done
    todo.save()

def reset_db():
    conn = sqlite3.connect('db.sqlite3')
    remove_all_todos(conn)
    remove_all_users(conn)
    conn.close()
    chase = add_user_after_reset("chase", "chase02", "chase@example.com", True)
    marshall = add_user_after_reset("marshall", "happypuppy", "mashall@example.com")
    skye = add_user_after_reset("skye", "skye04", "skye@example.com")
    you = add_user_after_reset("you", "you", "you@example.com")
    add_todo_after_reset(skye, chase, "take a bath")
    add_todo_after_reset(marshall, skye, "fly", True)
    add_todo_after_reset(chase, you, "some stupid chore")