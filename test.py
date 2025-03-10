import mysql.connector

pas = "root"

def connect_db():
    # return mysql.connector.connect(**DB_CONFIG)
    db =  mysql.connector.connect(
        host="localhost",
        user="root",
        password=pas,
    )
    
    c = db.cursor()
    
    c.execute("Show Databases")
    
    for i in c:
        print(i)


connect_db()