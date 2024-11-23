import sqlite3

class DatabaseManager:
    def __init__(self, db_name='user_data.db'):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the database and ensure required tables exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Create User table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
            ''')
            # Create Summary table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER,
                summary_text TEXT,
                FOREIGN KEY(userId) REFERENCES users(id)
            );
            ''')
            conn.commit()

    def get_user_by_email(self, email):
        """Fetch a user by email."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM users WHERE email = ?
            ''', (email,))
            return cursor.fetchone()

    def insert_user(self, name, email, password):
        """Insert a new user into the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO users (name, email, password) VALUES (?, ?, ?)
            ''', (name, email, password))
            conn.commit()

    def insert_summary(self, user_id, summary_text):
        """Insert a summary for a user."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO summaries (userId, summary_text) VALUES (?, ?)
            ''', (user_id, summary_text))
            conn.commit()

    def get_summary(self, user_id):
        """Fetch summaries by user ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM summaries WHERE userId = ?
            ''', (user_id,))
            return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Insert a new user
    db_manager.insert_user('Jane Doe', 'janedoe@example.com', 'securepassword')

    # Fetch the user by email
    user = db_manager.get_user_by_email('janedoe@example.com')
    print(f"User fetched by email: {user}")

    # Insert a summary
    if user:
        user_id = user[0]  # Assuming the ID is the first column
        db_manager.insert_summary(user_id, "This is Jane Doe's summary.")

    # Fetch summaries for the user
    summaries = db_manager.get_summary(user_id)
    print(f"Summaries for user {user_id}: {summaries}")
