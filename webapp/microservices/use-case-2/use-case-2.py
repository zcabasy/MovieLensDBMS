from flask import Flask, request
from flask_caching import Cache
import mariadb
import sys
from matplotlib.style import use
import numpy as np

use_case_2 = Flask(__name__)

use_case_2.config['CACHE_TYPE'] = 'SimpleCache'
use_case_2.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_2.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_2)

def connect():
    # f = open("mysql-user-db2.txt")
    # pwd = f.read()
    # f.close()
    pwd = "password"

    try:
        conn = mariadb.connect(
            user="safeuser",
            password=pwd,
            host="localhost",
            port=33082,
            database="MovieLensDB"
        )
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    

@use_case_2.route("/", methods=["GET", "POST"])
@cache.cached(timeout=300)
def query_table():
    movieId = 0

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT GROUP_CONCAT(ratings.rating) as rating FROM movies \
                INNER JOIN ratings ON movies.movieId = ratings.movieId \
                WHERE movies.movieId = %s;", (movieId, )) 

    # Parse response and create list
    ratings_list = []

    conn.close()

    mean = np.mean(ratings_list)
    std_dev = np.std(ratings_list)
    min = np.min(ratings_list)
    max = np.max(ratings_list)
    median = np.median(ratings_list)
    #Mode was not included here as a metric since ratings can take any continuous value so it is not very useful here

    return [ratings_list, mean, std_dev, min, max, median]

if __name__ == '__main__':
    use_case_2.run(debug = True, port = 5003, host="0.0.0.0")
