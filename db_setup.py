import mysql.connector

pas = "root"

def connect_db():
    # return mysql.connector.connect(**DB_CONFIG)
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=pas,
        database="fitapp"
    )

def setup_database():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
        """)

        print("users table created succefully.")

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS fitness_tracker (
        #     id INT AUTO_INCREMENT PRIMARY KEY,
        #     ,
        #     field2 VARCHAR(100)
        # );
        # """)

        # print("data_table table created succefully.")
        
        db.commit()
        db.close()
    except Exception as e:
        print(f"Database setup failed: {e}")


def create_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=pas
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS fitapp;")
    print("Database created successfully")
    setup_database()
    mydb.commit()
    mydb.close()
