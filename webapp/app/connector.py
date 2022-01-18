import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="password",
        host="localhost",
        port=3308,
        database="MovieLensDB"
    )
    
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("SELECT * FROM RatingsForPersonality LIMIT 11") 

for row in cur: 
    print(row)

conn.close()