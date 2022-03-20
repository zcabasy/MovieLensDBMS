from flask import Flask
from flask_caching import Cache, request
import mariadb
import sys

use_case_1 = Flask(__name__)

def connect():
        # f = open("mysql-user-db1.txt")
        # pwd = f.read()
        # f.close()
        pwd = "Za1lmx2vBB7DMjStnpvnhiT8SthxlTHh"
        
        try:
            conn = mariadb.connect(
                user="safebrowser",
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

@use_case_1.route("/",  methods=["GET"])
def get_genres():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Genres")
    genres = []
    for row in cur:
        genres.append(row[1].strip())
    return {'genres': genres}

def proc_params(data):
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

    return title, tag, genre, rating_lower, rating_upper, sort_by

@use_case_1.route("/",  methods=["POST"])
def query_table():
    data = request.form
    title, tag, genre, rating_lower, rating_upper, sort_by = proc_params(data)
    print(genre, flush=True)
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT Movies.movieId, Movies.title, GROUP_CONCAT(DISTINCT Tags.tag) as tags, AVG(Ratings.rating) as rating, GROUP_CONCAT(DISTINCT Genres.genre) as genre FROM Movies \
                LEFT JOIN Tags ON Movies.movieId = Tags.movieId \
                LEFT JOIN Ratings ON Movies.movieId = Ratings.movieId \
                LEFT JOIN Links ON Movies.movieId = Links.movieId \
                LEFT JOIN Movie_Genres ON Movies.movieId = Movie_Genres.movieId \
                INNER JOIN Genres ON Movie_Genres.genreId = Genres.genreId \
                WHERE Movies.movieId IN ( \
                SELECT Movies.movieId FROM Movies \
                LEFT JOIN Tags ON Movies.movieId = Tags.movieId \
                LEFT JOIN Ratings ON Movies.movieId = Ratings.movieId \
                LEFT JOIN Links ON Movies.movieId = Links.movieId \
                LEFT JOIN Movie_Genres ON Movies.movieId = Movie_Genres.movieId \
                INNER JOIN Genres ON Movie_Genres.genreId = Genres.genreId \
                WHERE title LIKE %s AND \
                (Tags.tag LIKE %s)  AND \
                (Genres.genre LIKE %s) \
                GROUP BY Movies.movieId \
                ) \
                AND (rating BETWEEN %s AND %s) \
                GROUP BY Movies.movieId \
                ORDER BY %s;", (title, tag, genre, rating_lower, rating_upper, sort_by))
    movies = []
    for row in cur:
        movie = {
            'movieId': row[0],
            'title': row[1],
            'tags': row[2].strip().split(","),
            'rating': row[3],
            'genres': row[4].strip().split(",")
        }
        movies.append(movie)
    conn.close()
    return {'movies': movies}



if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")
