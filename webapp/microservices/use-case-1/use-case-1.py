from flask import Flask
from flask_caching import Cache, request
import mariadb
import sys
from itertools import permutations
import itertools

use_case_1 = Flask(__name__)

use_case_1.config['CACHE_TYPE'] = 'SimpleCache'
use_case_1.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_1.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_1)

def connect():
        f = open("mysql-user-db1.txt")
        pwd = f.read()
        f.close()
        
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
@cache.cached(timeout=300)
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

    tag = data["tag"].split(",")
    genre = data["genre"].split(",")

    return title, tag, genre, rating_lower, rating_upper, sort_by

@use_case_1.route("/",  methods=["POST"])
def query_table():
    data = request.form
    title, tag, genre, rating_lower, rating_upper, sort_by = proc_params(data)
    
    # cached_val = cache.get(str([title, tag, genre, rating_lower, rating_upper, sort_by]))
    # if cached_val != None:
    #     return cached_val
    conn = connect()
    cur = conn.cursor()
    movies = []

    params = [(x,y) for x in tag for y in genre]
    for param in params:
        cur.execute("SELECT Movies.movieId, Movies.title, GROUP_CONCAT(DISTINCT Tags.tag) as tags, AVG(Ratings.rating) as rating, GROUP_CONCAT(DISTINCT Genres.genre) as genre FROM Movies \
                    LEFT JOIN Tags ON Movies.movieId = Tags.movieId \
                    LEFT JOIN Ratings ON Movies.movieId = Ratings.movieId \
                    LEFT JOIN Movie_Genres ON Movies.movieId = Movie_Genres.movieId \
                    INNER JOIN Genres ON Movie_Genres.genreId = Genres.genreId \
                    WHERE Movies.movieId IN ( \
                    SELECT Movies.movieId FROM Movies \
                    LEFT JOIN Tags ON Movies.movieId = Tags.movieId \
                    LEFT JOIN Movie_Genres ON Movies.movieId = Movie_Genres.movieId \
                    INNER JOIN Genres ON Movie_Genres.genreId = Genres.genreId \
                    WHERE title LIKE %s AND \
                    (Tags.tag LIKE %s)  AND \
                    (Genres.genre LIKE %s) \
                    GROUP BY Movies.movieId \
                    ) \
                    GROUP BY Movies.movieId \
                    HAVING AVG(Ratings.rating) BETWEEN %s AND %s;", (title, "%"+param[0]+"%", "%"+param[1]+"%", rating_lower, rating_upper))
        
        for row in cur:
            movie = {
                'movieId': row[0],
                'title': row[1],
                'tags': row[2].strip().split(","),
                'rating': row[3],
                'genres': row[4].strip().split(",")
            }
            if movie not in movies:
                movies.append(movie)
    
    conn.close()

    # cache.set(str([title, tag, genre, rating_lower, rating_upper, sort_by]), {'movies': movies})
    
    if sort_by == 'rating DESC':
        movies = sorted(movies, key=lambda d: d['rating'], reverse=True)
    elif sort_by == 'rating ASC':
        movies = sorted(movies, key=lambda d: d['rating'])
    elif sort_by == 'title ASC':
        movies = sorted(movies, key=lambda d: d['title'])
    else:
        movies = sorted(movies, key=lambda d: d['title'], reverse=True)
    return {'movies': movies}



if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")
