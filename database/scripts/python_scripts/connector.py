import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "my-secret-pw"
)

mycursor = db.cursor()

#database = "MovieLensDB"