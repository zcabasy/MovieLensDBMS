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
    # f = open("mysql-user-db3.txt"); pwd = f.read(); f.close()
    pwd = "CNuDHdcW3DIc5DL37ZDZpnwYQO4ONp3n"

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
        # get 10 popular and polarising movies
        return get_popular_and_polarising_movies(10)
    elif request.method == "POST":
        # get user-requested-number of popular and polarising movies
        req = request.form
        num = req.get("num")
        return get_popular_and_polarising_movies(num)
    
def get_popular_and_polarising_movies(num):
    popular_movies = get_popular_movies(num)
    polarising_movies = get_polarising_movies(num)
    return {
        "popular_movies": popular_movies,
        "polarising_movies": polarising_movies
    }

def get_popular_movies(num):
    query = f"SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
        MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, COUNT(Ratings.rating) as num_ratings \
        FROM Genres INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
        INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
        GROUP BY genre \
        ORDER BY rating DESC, std_rating ASC, min_rating DESC, max_rating DESC, num_ratings DESC \
        LIMIT {num};"
    return get_movies(query)

def get_polarising_movies(num):
    query = f"SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
        MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, MAX(Ratings.rating) - MIN(Ratings.rating) as range_rating, \
        COUNT(Ratings.rating) as num_ratings \
        FROM Genres \
        INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
        INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
        GROUP BY genre \
        ORDER BY std_rating DESC, range_rating DESC, num_ratings DESC \
        LIMIT {num};"
    return get_movies(query)

def get_movies(query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
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
    cur.close()
    
    return movies


if __name__ == '__main__':
    use_case_3.run(debug = True, port = 5004, host="0.0.0.0")
