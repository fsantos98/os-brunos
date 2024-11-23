import pymysql
import pymysql.cursors

class DatabaseManager:
    def __init__(self, db_name, user, password, host='localhost', port=3306):
        self.connection_params = {
            'host': host,
            'user': user,
            'password': password,
            'database': db_name,
            'port': port,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'connect_timeout': 10,
            'read_timeout': 10,
            'write_timeout': 10,
        }
        self._initialize_database()

    def _connect(self):
        """Establish a connection to the database."""
        try:
            return pymysql.connect(**self.connection_params)
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def _initialize_database(self):
        """Initialize the database and ensure required tables exist."""
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                # Create Users table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                );
                ''')
                # Create Summaries table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS summaries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    userId INT,
                    summary_text TEXT,
                    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
                );
                ''')
                connection.commit()
        finally:
            connection.close()

    def get_user_by_email(self, email):
        """Fetch a user by email."""
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                return cursor.fetchone()
        finally:
            connection.close()

    def insert_user(self, name, email, password):
        """Insert a new user into the database."""
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                    (name, email, password)
                )
                connection.commit()
                return cursor.lastrowid  # Return the new user's ID
        finally:
            connection.close()

    def insert_summary(self, user_id, summary_text):
        """Insert a summary for a user."""
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO summaries (userId, summary_text) VALUES (%s, %s)',
                    (user_id, summary_text)
                )
                connection.commit()
        finally:
            connection.close()

    def get_summary(self, user_id):
        """Fetch summaries by user ID."""
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM summaries WHERE userId = %s', (user_id,))
                return cursor.fetchall()
        finally:
            connection.close()


# Example usage
if __name__ == "__main__":
    # Replace with your MySQL database credentials
    db_manager = DatabaseManager(
        db_name='defaultdb',
        user='avnadmin',
        password='AVNS_U-c1ezivY9TcPqqXrwg',
        host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
        port=18173
    )

    # Insert a new user
    user_id = db_manager.insert_user('Jane Doe', 'janedoe@example.com', 'securepassword')
    print(f"New user ID: {user_id}")

    # Fetch the user by email
    user = db_manager.get_user_by_email('janedoe@example.com')
    print(f"User fetched by email: {user}")

    # Insert a summary
    db_manager.insert_summary(user_id, "This is Jane Doe's summary.")

    # Fetch summaries for the user
    summaries = db_manager.get_summary(user_id)
    print(f"Summaries for user {user_id}: {summaries}")
