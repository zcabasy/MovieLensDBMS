from flask import Flask, request
from flask_caching import Cache
import mariadb
import numpy as np
import sys

use_case_3 = Flask(__name__)

use_case_3.config['CACHE_TYPE'] = 'SimpleCache'
use_case_3.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_3.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_3)

def connect():
    f = open("mysql-user-db3.txt")
    pwd = f.read()
    f.close()

    try:
        conn = mariadb.connect(
            user="safebrowser",
            password=pwd,
            host="db-3",
            port=3306,
            database="MovieLensDB"
        )
        print("connected 3", flush=True)
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    

@use_case_3.route("/", methods=["GET", "POST"])
@cache.cached(timeout=300)
def query_table():
    if request.method == "GET":
        # get 10 popular and polarising genres
        return get_popular_and_polarising_genres(10)
    elif request.method == "POST":
        pass
        # # get user-requested-number of popular and polarising genres
        # req = request.form
        # num = req.get("num")
        # return get_popular_and_polarising_genres(num)
    
def get_popular_and_polarising_genres(num):
    popular_genres = get_popular_genres(num)
    polarising_genres = get_polarising_genres(num)
    return {
        "popular_genres": popular_genres,
        "polarising_genres": polarising_genres
    }

def get_popular_genres(num):
    query = f"SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
        MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, COUNT(Ratings.rating) as num_ratings \
        FROM Genres INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
        INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
        GROUP BY genre \
        ORDER BY rating DESC, std_rating ASC, min_rating DESC, max_rating DESC, num_ratings DESC \
        LIMIT {num};"
    return get_genres(query, "popular")

def get_polarising_genres(num):
    query = f"SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
        MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, MAX(Ratings.rating) - MIN(Ratings.rating) as range_rating, \
        COUNT(Ratings.rating) as num_ratings \
        FROM Genres \
        INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
        INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
        GROUP BY genre \
        ORDER BY std_rating DESC, range_rating DESC, num_ratings DESC \
        LIMIT {num};"
    return get_genres(query, "polarising")

def get_genres(query, popular_or_polarising):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    genres = []
    for row in cur:
        genre = {
            "genre": row[0].strip(),
            "rating": row[1],
            "std_rating": row[2],
            "min_rating": row[3],
            "max_rating": row[4],
            "num_ratings": row[5] if popular_or_polarising == "popular" else row[6]
        }
        if popular_or_polarising == "polarising":
            genre["range_rating"] = row[5]
        genres.append(genre)
    conn.close()
    
    return genres


if __name__ == '__main__':
    use_case_3.run(debug = True, port = 5004, host="0.0.0.0")
