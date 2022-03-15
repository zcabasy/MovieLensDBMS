from flask import Flask, request
from flask_caching import Cache
import mariadb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import sys
from joblib import dump, load
from os.path import exists

use_case_4 = Flask(__name__)

use_case_4.config['CACHE_TYPE'] = 'SimpleCache'
use_case_4.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_4.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_4)

def connect():
    # f = open("mysql-user-db4.txt")
    # pwd = f.read()
    # f.close()
    pwd = "password"

    try:
        conn = mariadb.connect(
            user="safeuser",
            password=pwd,
            host="localhost",
            port=33084,
            database="MovieLensDB"
        )
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def sql_to_pandas():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT Ratings.movieId, GROUP_CONCAT(Ratings.rating) as ratings, COUNT(Ratings.rating) as num_ratings \
                FROM Ratings \
                GROUP BY movieId \
                ORDER BY num_ratings DESC;")

    df = pd.DataFrame()

    for row in cur:
        name = row[0]
        
        ratings = row[1]
        ratings = ratings.split(",")
        ratings_map = map(float, ratings)
        ratings = list(ratings_map)
        actual_mean = np.mean(ratings)
        num_ratings = len(ratings)
        
        if num_ratings == 2 or num_ratings == 3 or num_ratings == 4:
            ratings = ratings[0:1] # make this random
        if num_ratings > 4:
            threshold = 0.2 * num_ratings
            ratings = ratings[0:int(threshold)] # make this random
        
        mean = np.mean(ratings)
        std = np.std(ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)
        sample_size = len(ratings)
        
        row = pd.Series([name, mean, std, min_rating, max_rating, sample_size, actual_mean])
        row_df = pd.DataFrame([row])
        df = pd.concat([df, row_df], ignore_index=True)

    conn.close()
    df.columns = ['Movie', 'Mean', 'Std', 'Min', 'Max', 'Sample', 'Actual']

    return df

def train_model():
    df = sql_to_pandas()
    X = df.drop('Actual', axis=1)
    X = X.drop('Movie', axis = 1)
    y = df.pop('Actual')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle = True)

    clf = SVR().fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    score = mean_squared_error(y_test, y_pred)
    
    return clf, score

def data_for_given_movie(movieId):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT Ratings.movieId, GROUP_CONCAT(Ratings.rating) as ratings, COUNT(Ratings.rating) as num_ratings \
                FROM Ratings \
                WHERE movieId = %s;", (movieId, ))

    for row in cur:
        name = row[0]
        ratings = row[1]
        ratings = ratings.split(",")
        ratings_map = map(float, ratings)
        ratings = list(ratings_map)
        actual_mean = np.mean(ratings)
        num_ratings = len(ratings)

        if num_ratings == 2 or num_ratings == 3 or num_ratings == 4:
            ratings = ratings[0:1] # make this random
        if num_ratings > 4:
            threshold = 0.2 * num_ratings
            ratings = ratings[0:int(threshold)] # make this random

        mean = np.mean(ratings)
        std = np.std(ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)
        sample_size = len(ratings)

        row = pd.Series([name, mean, std, min_rating, max_rating, sample_size, actual_mean])
        df = pd.DataFrame([row])
        df.columns = ['Movie', 'Mean', 'Std', 'Min', 'Max', 'Sample', 'Actual']
        X = df.drop('Actual', axis=1)
        X = X.drop('Movie', axis=1)
        y = df.pop('Actual')
        return [X, y]


@use_case_4.route("/", methods=["GET", "POST"])
@cache.cached(timeout=300)
def predict_rating():
    
    movieId = 0
    
    data = data_for_given_movie(movieId)
    X_test = data[0]
    y_test = data[1]

    if exists('clf.joblib'):
        clf = load('clf.joblib')
    else:
        clf, score = train_model()
        dump(clf, 'clf.joblib')
    
    y_pred = clf.predict(X_test)

    score = mean_squared_error(y_test, y_pred)
    return [score, X_test, y_test, y_pred]
    

if __name__ == '__main__':
    use_case_4.run(debug = True, port = 5005, host="0.0.0.0")
