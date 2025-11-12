import mysql.connector
from mysql.connector import pooling, Error
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'server'),
    'password': os.getenv('DB_PASS', 'password'),
    'database': os.getenv('DB_NAME', 'db'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Connection pool for high performance
POOL = pooling.MySQLConnectionPool(
    pool_name="nexora_pool",
    pool_size=10,
    **DB_CONFIG
)

@contextmanager
def db_cursor():
    conn = None
    cursor = None
    try:
        conn = POOL.get_connection()
        cursor = conn.cursor(dictionary=True)
        yield cursor
        conn.commit()
    except Error as e:
        print(f"[DB ERROR] {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ---------------- USERS ----------------
def create_user(username, gmail, password, role, enabled=True):
    query = """
        INSERT INTO users (UserName, Gmail, PasswordHash, Roles, EnabledUser)
        VALUES (%s, %s, SHA2(%s, 256), %s, %s);
    """
    with db_cursor() as cur:
        cur.execute(query, (username, gmail, password, role, enabled))

def delete_user(user_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM users WHERE ID = %s;", (user_id,))

def change_user_role(user_id, role_id):
    with db_cursor() as cur:
        cur.execute("UPDATE users SET Roles = %s WHERE ID = %s;", (role_id, user_id))

def change_user_password(user_id, new_password):
    with db_cursor() as cur:
        cur.execute("UPDATE users SET PasswordHash = SHA2(%s, 256) WHERE ID = %s;", (new_password, user_id))

def change_user_field(user_id, field, value):
    allowed = ['UserName', 'Gmail', 'EnabledUser']
    if field not in allowed:
        raise ValueError("Invalid field name")
    with db_cursor() as cur:
        cur.execute(f"UPDATE users SET {field} = %s WHERE ID = %s;", (value, user_id))

def get_user(user_id):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE ID = %s;", (user_id,))
        return cur.fetchone()

# ---------------- ROLES ----------------
def create_role(role_name):
    with db_cursor() as cur:
        cur.execute("INSERT INTO roles (RoleName) VALUES (%s);", (role_name,))

def delete_role(role_id):
    with db_cursor() as cur:
        cur.execute("UPDATE users SET Roles = 2 WHERE Roles = %s;", (role_id,))
        cur.execute("DELETE FROM roles_actions WHERE roleID = %s;", (role_id,))
        cur.execute("DELETE FROM roles WHERE ID = %s;", (role_id,))

def add_action_to_role(role_id, action_id):
    with db_cursor() as cur:
        cur.execute("INSERT INTO roles_actions (roleID, actionID) VALUES (%s, %s);", (role_id, action_id))

# ---------------- ACTIONS ----------------
def create_action(name, desc=None):
    with db_cursor() as cur:
        cur.execute("INSERT INTO actions (ActionName, ActionDesc) VALUES (%s, %s);", (name, desc))

def delete_action(action_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM roles_actions WHERE actionID = %s;", (action_id,))
        cur.execute("DELETE FROM actions WHERE ID = %s;", (action_id,))

# ---------------- CHAT ----------------
def create_chat(chat_name):
    with db_cursor() as cur:
        cur.execute("INSERT INTO chat (ChatName) VALUES (%s);", (chat_name,))

def delete_chat(chat_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM msg WHERE Chat = %s;", (chat_id,))
        cur.execute("DELETE FROM chat WHERE ID = %s;", (chat_id,))

# ---------------- MESSAGES ----------------
def send_message(user_id, chat_id, msg):
    with db_cursor() as cur:
        cur.execute("""
            INSERT INTO msg (Edited, User, Chat, DateInf, MSG)
            VALUES (FALSE, %s, %s, NOW(), %s);
        """, (user_id, chat_id, msg))

def edit_message(msg_id, new_msg):
    with db_cursor() as cur:
        cur.execute("UPDATE msg SET Edited = TRUE, MSG = %s WHERE ID = %s;", (new_msg, msg_id))

def delete_message(msg_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM msg WHERE ID = %s;", (msg_id,))

def get_chat_messages(chat_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT m.ID, u.UserName, m.MSG, m.DateInf, m.Edited
            FROM msg m
            JOIN users u ON m.User = u.ID
            WHERE m.Chat = %s
            ORDER BY m.DateInf ASC;
        """, (chat_id,))
        return cur.fetchall()