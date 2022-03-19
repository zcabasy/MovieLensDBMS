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
    pwd = "5PV8frCZdsu2ePPorMhIs5tofGGw3yfP"

    try:
        conn = mariadb.connect(
            user="safebrowser",
            password=pwd,
            host="db-2",
            port=3306,
            database="MovieLensDB"
        )
        print("connected 2", flush=True)
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    

@use_case_2.route("/", methods=["POST"])
def query_table():
    data = request.form
    movieId = int(data["movieId"])
    
    cached_val = cache.get(movieId)
    if cached_val != None:
        return cached_val
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT GROUP_CONCAT(Ratings.rating) as rating FROM Ratings WHERE Ratings.movieId = %s;", (movieId, )) 

    # Parse response and create list
    ratings_list = []
    for row in cur:
        ratings_list = list(map(float, row[0].split(",")))

    conn.close()

    mean = np.mean(ratings_list)
    std_dev = np.std(ratings_list)
    min = np.min(ratings_list)
    max = np.max(ratings_list)
    median = np.median(ratings_list)
    #Mode was not included here as a metric since ratings can take any continuous value so it is not very useful here
    
    #return_val = [ratings_list, mean, std_dev, min, max, median]
    return_val = {
        "ratings_list": ratings_list,
        "std_dev": std_dev,
        "min": min,
        "max":max,
        "median":median
    }
    cache.set(movieId, return_val)
    return return_val

if __name__ == '__main__':
    use_case_2.run(debug = True, port = 5003, host="0.0.0.0")
