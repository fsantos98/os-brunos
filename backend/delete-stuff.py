import pymysql
import pymysql.cursors
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    def _initialize_database(self):
        """Verify database connectivity and perform initialization if necessary."""
        try:
            connection = self._connect()
            logging.info("Database connection successfully established.")
            connection.close()
        except Exception as e:
            logging.error(f"Failed to initialize database: {e}")
            raise

    def _connect(self):
        """Establish a connection to the database."""
        try:
            return pymysql.connect(**self.connection_params)
        except pymysql.MySQLError as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    def delete_summary_by_user_id(self, user_id):
        """Delete summaries by user ID."""
        logging.info(f"Attempting to delete summaries for user ID: {user_id}")
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                query = 'DELETE FROM summaries WHERE Id = %s'
                cursor.execute(query, (user_id,))
                connection.commit()  # Commit the transaction
                logging.info(f"{cursor.rowcount} rows deleted.")
                return cursor.rowcount
        except pymysql.MySQLError as e:
            logging.error(f"Error occurred while deleting summaries for user {user_id}: {e}")
            raise
        finally:
            connection.close()

# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager(
        db_name='testdb',
        user='avnadmin',
        password='AVNS_U-c1ezivY9TcPqqXrwg',
        host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
        port=18173
    )

    try:
        #deleted_rows = db_manager.delete_summary_by_user_id(2)
        print(f"Deleted rows: {deleted_rows}")
    except Exception as e:
        print(f"An error occurred: {e}")
