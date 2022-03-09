from flask import Flask
from flask_caching import Cache
import mariadb
import numpy as np
import sys

use_case_3 = Flask(__name__)

cache = Cache()
cache.init_app(use_case_3)
use_case_3.config['CACHE_TYPE'] = 'SimpleCache'

def connect():
    # f = open("mysql-user-db3.txt")
    # pwd = f.read()
    # f.close()
    pwd = "password"

    try:
        conn = mariadb.connect(
            user="safeuser",
            password=pwd,
            host="localhost",
            port=33083,
            database="MovieLensDB"
        )
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    

@use_case_3.route("/")
def query_table():

    conn = connect()
    cur = conn.cursor()
    # Popular Movies Query
    cur.execute("SELECT movies.title, AVG(ratings.rating) as avg_rating, stddev(ratings.rating) as std_rating, \
                MIN(ratings.rating) as min_rating, MAX(ratings.rating) as max_rating, COUNT(ratings.rating) as num_ratings \
                FROM movies INNER JOIN ratings ON movies.movieId = ratings.movieId \
                GROUP BY title \
                ORDER BY num_ratings DESC, avg_rating DESC, std_rating ASC\
                LIMIT 10;") 

    #Parse response
    popular_response  = ""

    # Polarising Movies Query
    cur.execute("SELECT movies.title, AVG(ratings.rating) as avg_rating, stddev(ratings.rating) as std_rating, \
                MIN(ratings.rating) as min_rating, MAX(ratings.rating) as max_rating, COUNT(ratings.rating) as num_ratings \
                FROM movies INNER JOIN ratings ON movies.movieId = ratings.movieId \
                GROUP BY title \
                ORDER BY std_rating DESC, num_ratings DESC \
                LIMIT 10;") 

    #Parse response
    polarising_response  = ""

    
    return [popular_response, polarising_response]

if __name__ == '__main__':
    use_case_3.run(debug = True, port = 5004, host="0.0.0.0")