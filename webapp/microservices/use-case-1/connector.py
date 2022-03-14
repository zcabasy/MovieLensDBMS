import mariadb
import sys

# f = open("./mysql-user-db1.txt")
# pwd = f.read()
# f.close()

# try:
#     conn = mariadb.connect(
#         user="safeuser",
#         password="password",
#         host="localhost",
#         port=33082,
#         database="MovieLensDB"
#     )
    
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

# # Get Cursor
# cur = conn.cursor()

# cur.execute("SELECT * FROM Tags LIMIT 1") 

# for row in cur: 
#     print(row)

# conn.close()