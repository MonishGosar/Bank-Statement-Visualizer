import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='pain7@21',
            database='bank'
        )
        print("Successfully connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        upi VARCHAR(255),
        withdrawal DECIMAL(10, 2),
        deposited DECIMAL(10, 2),
        balance DECIMAL(10, 2)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: '{e}'")
        print(f"SQL Query: {create_table_query}")

def main():
    connection = create_connection()
    if connection is not None:
        create_table(connection)
        connection.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
