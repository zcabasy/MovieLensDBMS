from flask import Flask
from flask_caching import Cache
import mariadb
import sys

use_case_1 = Flask(__name__)

cache = Cache()
cache.init_app(use_case_1)
use_case_1.config['CACHE_TYPE'] = 'SimpleCache'

def connect():
    # f = open("mysql-user-db1.txt")
    # pwd = f.read()
    # f.close()
    pwd = "password"

    try:
        conn = mariadb.connect(
            user="safeuser",
            password=pwd,
            host="localhost",
            port=3308,
            database="MovieLensDB"
        )
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    

@use_case_1.route("/")
def query_table():
    # Do not remove % signs from strings below, needed for regex matching in sql. Instead, add user content in between
    title = "%--%"
    rating_lower = 0
    rating_upper = 5
    tag = "%--%"
    genre = "%--%"

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT title, tag, rating, genreId FROM movielens \
                    WHERE title LIKE '%s' AND \
                    tag LIKE '%s'  AND \
                    (genreId LIKE '%s') AND \
                    rating BETWEEN %s AND %s \
                    ORDER BY %s;", (title, tag, genre, rating_lower, rating_upper)) 
    
    # Parse response and package into something that can be returned e.g. JSON
    response = ""

    conn.close()
    
    return response

if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")