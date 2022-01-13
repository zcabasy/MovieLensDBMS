import mysql.connector

db = mysql.connector.connect(
    host = "127.0.0.1:33061",
    user = "some-mysql2",
    password = "my-secret-pw"
)

#mycursor = db.cursor()

#database = "MovieLensDB"