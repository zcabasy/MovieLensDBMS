from flask import Flask
from flask_caching import Cache, request
import mariadb
import sys

use_case_1 = Flask(__name__)

use_case_1.config['CACHE_TYPE'] = 'SimpleCache'
use_case_1.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_1.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_1)

def connect():
        # f = open("mysql-user-db1.txt")
        # pwd = f.read()
        # f.close()
        pwd = "password"

        try:
            conn = mariadb.connect(
                user="safebrowser",
                password=pwd,
                host="localhost",
                port=3308,
                database="MovieLensDB"
            )
            return conn
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
@use_case_1.route("/",  methods=["POST"])
# @cache.cached(timeout=300)
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
    cur.execute("SELECT movieId, title, tag, rating, genre FROM movielens \
        WHERE title LIKE %s AND \
        (tag LIKE %s)  AND \
        (genre LIKE %s) AND \
        rating BETWEEN %s AND %s \
        ORDER BY %s;", (title, tag, genre, rating_lower, rating_upper, sort_by))
    
    # Parse response and package into something that can be returned e.g., JSON
    response = ""
    
    conn.close()
    
    return response

if __name__ == '__main__':
    
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")
