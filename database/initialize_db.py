from database_connection import DatabaseConnection

def initialize_db():
    db_connection = DatabaseConnection()

    # Create users table without chat_histories column
    users_query = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT,
        password TEXT NOT NULL,
        full_name TEXT,
        disabled INTEGER NOT NULL DEFAULT 0,
        credits INTEGER NOT NULL DEFAULT 0
    );
    """
    db_connection.execute_query(users_query)

    # Create chat_histories table with a foreign key reference to users
    chat_histories_query = """
    CREATE TABLE IF NOT EXISTS chat_histories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key INTEGER NOT NULL,
        username TEXT NOT NULL,
        history TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users (username)
    );

    """
    db_connection.execute_query(chat_histories_query)

if __name__ == "__main__":
    initialize_db()