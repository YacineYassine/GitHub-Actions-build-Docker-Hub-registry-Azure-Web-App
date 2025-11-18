import sqlite3
import os

def init_db():
    """Initialiser la base de données SQLite"""
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/feedbacks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sepal_length REAL,
            sepal_width REAL,
            petal_length REAL,
            petal_width REAL,
            prediction TEXT,
            approved BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_feedback(features, prediction, approved):
    """Sauvegarder un feedback utilisateur"""
    conn = sqlite3.connect('database/feedbacks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedbacks 
        (sepal_length, sepal_width, petal_length, petal_width, prediction, approved)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (*features, prediction, approved))
    
    conn.commit()
    conn.close()