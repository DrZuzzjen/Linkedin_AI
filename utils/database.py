import sqlite3
import os

class Database:
    def __init__(self, db_name='linkedin_automation.db'):
        # Ensure the data directory exists
        os.makedirs('/app/data', exist_ok=True)
        self.conn = sqlite3.connect(f'/app/data/{db_name}')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def insert_post(self, post):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO posts (title, author, summary)
        VALUES (?, ?, ?)
        ''', (post['title'], post['author'], post['summary']))
        self.conn.commit()

    def get_recent_posts(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM posts ORDER BY created_at DESC LIMIT ?', (limit,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()

    def save_linkedin_token(self, access_token, refresh_token, expires_at):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO linkedin_auth (id, access_token, refresh_token, expires_at)
        VALUES (1, ?, ?, ?)
        ''', (access_token, refresh_token, expires_at))
        self.conn.commit()

    def get_linkedin_token(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT access_token, refresh_token, expires_at FROM linkedin_auth WHERE id = 1')
        return cursor.fetchone() 