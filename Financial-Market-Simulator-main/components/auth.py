import sqlite3
import streamlit as st
from hashlib import sha256

DB_PATH = "data/users.db"

def init_auth_db():
    """Initialize the database with the necessary table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            points INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash the password using sha256."""
    return sha256(password.encode()).hexdigest()

def authenticate_user():
    """Authenticate user using username and password."""
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        hashed_password = hash_password(password)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username=? AND password=?
        """, (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return user[0]  # return username if authentication is successful
        else:
            st.sidebar.error("Invalid username or password.")
    return None

def register_user():
    """Register a new user."""
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    confirm_password = st.sidebar.text_input("Confirm Password", type="password")

    if st.sidebar.button("Register"):
        if password != confirm_password:
            st.sidebar.error("Passwords do not match.")
        else:
            hashed_password = hash_password(password)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, password) VALUES (?, ?)
                """, (username, hashed_password))
                conn.commit()
                conn.close()
                return True
            except sqlite3.IntegrityError:
                st.sidebar.error("Username already exists.")
    return False

def get_current_user(username):
    """Fetch the current user's data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE username=?
    """, (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"username": user[0], "points": user[2]}  # Example of user data (username, points)
    else:
        return None

# Initialize the authentication database
init_auth_db()

