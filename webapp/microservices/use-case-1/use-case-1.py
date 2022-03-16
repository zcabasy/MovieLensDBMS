from flask import Flask
from flask_caching import Cache, request
import mariadb
import sys

use_case_1 = Flask(__name__)

def connect():
        # f = open("mysql-user-db1.txt")
        # pwd = f.read()
        # f.close()
        pwd = "password"
        
        try:
            conn = mariadb.connect(
                user="root",
                password=pwd,
                host="db-1",
                port=3306,
                database="MovieLensDB"
            )
            print("connected 1", flush=True)
            return conn
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
@use_case_1.route("/",  methods=["POST"])
def query_table():
    data = request.form
    title = "%" + data["title"] + "%"
    rating_lower = int(data["min_rating"])
    rating_upper = int(data["max_rating"])
    sort_by = data["sort_by"]

    org_tag = data["tag"].split(",")
    tag = ""
    for x in range(len(org_tag)):
        if x == 0:
            tag += "%" + org_tag[x] + "%"
        else:
            tag += " OR tag LIKE %" + org_tag[x] + "%"
    
    org_genre = data["genre"].split(",")
    genre = ""
    for x in range(len(org_genre)):
        if x == 0:
            genre += "%" + org_genre[x] + "%"
        else:
            genre += " OR genre LIKE %" + org_genre[x] + "%"
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT Movies.movieId, Movies.title, GROUP_CONCAT(DISTINCT Tags.tag), AVG(Ratings.rating), GROUP_CONCAT(DISTINCT Genres.genre) FROM Movies \
                LEFT JOIN Tags ON Movies.movieId = Tags.movieId \
                LEFT JOIN Ratings ON Movies.movieId = Ratings.movieId \
                LEFT JOIN Links ON Movies.movieId = Links.movieId \
                LEFT JOIN Movie_Genres ON Movies.movieId = Movie_Genres.movieId \
                INNER JOIN Genres ON Movie_Genres.genreId = Genres.genreId \
                WHERE title LIKE %s AND \
                (tag LIKE %s)  AND \
                (genre LIKE %s) AND \
                (rating BETWEEN %s AND %s) \
                ORDER BY %s;", (title, tag, genre, rating_lower, rating_upper, sort_by))
    
    # Parse response and package into something that can be returned e.g., JSON
    response = ""
    
    conn.close()
    
    return response

if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")
