from flask import Flask, request
from flask_caching import Cache
import mariadb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from joblib import dump, load
from os.path import exists
from sklearn.preprocessing import StandardScaler

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
    pwd = "RQXzvGedPmTIun25FVoujDgCepMIkPKG"

    try:
        conn = mariadb.connect(
            user="safebrowser",
            password=pwd,
            host="db-4",
            port=3306,
            database="MovieLensDB"
        )
        print("connected 4", flush=True)
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def gen_dataset():
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

    df.to_csv('dataset-4.csv', index=False)
    
    X = df.drop('Actual', axis=1)
    X = X.drop('Movie', axis = 1)
    y = df.pop('Actual')

    return X, y

def train_model():
    if exists('dataset-4.csv'):
        df = pd.read_csv('dataset-4.csv')
        X = df.drop('Actual', axis=1)
        X = X.drop('Movie', axis = 1)
        y = df.pop('Actual')
    else:
        X, y = gen_dataset()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle = True)

    clf = SVR().fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    score = mean_absolute_error(y_test, y_pred)
    
    return clf, score

def data_for_given_movie(movieId):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT Ratings.movieId, GROUP_CONCAT(Ratings.rating) as ratings, COUNT(Ratings.rating) as num_ratings \
                FROM Ratings \
                WHERE movieId = %s;", (movieId, ))

    for row in cur:
        #Only one result since we specify movieId which is unique
        name = row[0]
        ratings = row[1]
        ratings = ratings.split(",")
        ratings_map = map(float, ratings)
        ratings = list(ratings_map)

        #Full stats
        actual_mean = np.mean(ratings)
        actual_std = np.std(ratings)
        actual_min_rating = min(ratings)
        actual_max_rating = max(ratings)
        num_ratings = len(ratings)
        full_stats = [actual_mean, actual_std, actual_min_rating, actual_max_rating, num_ratings]

        if num_ratings == 2 or num_ratings == 3 or num_ratings == 4:
            ratings = ratings[0:1] # make this random
        if num_ratings > 4:
            threshold = 0.2 * num_ratings
            ratings = ratings[0:int(threshold)] # make this random

        #Subset Stats
        mean = np.mean(ratings)
        std = np.std(ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)
        sample_size = len(ratings)
        subset_stats = [mean, std, min_rating, max_rating, sample_size]

        row = pd.Series([name, mean, std, min_rating, max_rating, sample_size, actual_mean])
        df = pd.DataFrame([row])
        df.columns = ['Movie', 'Mean', 'Std', 'Min', 'Max', 'Sample', 'Actual']
        X = df.drop('Actual', axis=1)
        X = X.drop('Movie', axis=1)
        y = df.pop('Actual')
        return [X, y, subset_stats, full_stats]


@use_case_4.route("/", methods=["GET", "POST"])
def predict_rating():
    
    data = request.form
    movieId = int(data["movieId"])

    cached_val = cache.get(movieId)
    if cached_val != None:
        return cached_val

    data = data_for_given_movie(movieId)
    X_test = data[0]
    y_test = data[1]
    subset_stats = data[2]
    full_stats = data[3]

    if exists('clf.joblib'):
        clf = load('clf.joblib')
    else:
        clf, score = train_model()
        dump(clf, 'clf.joblib')
    
    y_pred = clf.predict(X_test)

    score = mean_absolute_error(y_test, y_pred)
    return_val = [score, y_test, y_pred, subset_stats, full_stats]
    cache.set(movieId, return_val)
    return return_val
    

if __name__ == '__main__':
    use_case_4.run(debug = True, port = 5005, host="0.0.0.0")
