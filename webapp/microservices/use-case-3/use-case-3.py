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
    # f = open("mysql-user-db3.txt")
    # pwd = f.read()
    # f.close()
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
    

@use_case_3.route("/", methods=["POST"])
@cache.cached(timeout=300)
def query_table():
    conn = connect()
    cur = conn.cursor()
    # Popular Movies Query
    cur.execute("SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
                MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, COUNT(Ratings.rating) as num_ratings \
                FROM Genres INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
                INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
                GROUP BY genre \
                ORDER BY rating DESC, std_rating ASC, min_rating DESC, max_rating DESC, num_ratings DESC \
                LIMIT 10;")

    #Parse response
    popular_response  = ""

    # Polarising Movies Query
    cur.execute("SELECT Genres.genre, AVG(Ratings.rating) AS rating, stddev(Ratings.rating) as std_rating, \
                MIN(Ratings.rating) as min_rating, MAX(Ratings.rating) as max_rating, MAX(Ratings.rating) - MIN(Ratings.rating) as range_rating, \
                COUNT(Ratings.rating) as num_ratings \
                FROM Genres \
                INNER JOIN Movie_Genres ON Genres.genreId = Movie_Genres.genreId \
                INNER JOIN Ratings ON Movie_Genres.movieId = Ratings.movieId \
                GROUP BY genre \
                ORDER BY std_rating DESC, range_rating DESC, num_ratings DESC \
                LIMIT 10;")

    #Parse response
    polarising_response  = ""
    
    return [popular_response, polarising_response]

if __name__ == '__main__':
    use_case_3.run(debug = True, port = 5004, host="0.0.0.0")
