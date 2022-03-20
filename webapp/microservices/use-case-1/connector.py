import mariadb
import sys

# f = open("./mysql-user-db1.txt")
# pwd = f.read()
# f.close()

try:
    conn = mariadb.connect(
        user="safebrowser",
        password="password",
        host="db-1",
        port=3306,
        database="MovieLensDB"
    )
    print("connected 1", flush=True)
    
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
