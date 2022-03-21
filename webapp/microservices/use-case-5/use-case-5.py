from flask import Flask, request
from flask_caching import Cache
import mariadb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import sys
from joblib import dump, load
from os.path import exists
import statistics

use_case_5 = Flask(__name__)

use_case_5.config['CACHE_TYPE'] = 'SimpleCache'
use_case_5.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_5.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_5)

def connect():
    f = open("mysql-user-db5.txt")
    pwd = f.read()
    f.close()

    try:
        conn = mariadb.connect(
            user="safebrowser",
            password=pwd,
            host="db-5",
            port=3306,
            database="MovieLensDB"
        )
        print("connected 5", flush=True)
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def person_traits_agg(movieId):
    # Return aggregate stats on personality traits of users who gave the film a high rating
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT GROUP_CONCAT(Personality.openness), \
                GROUP_CONCAT(Personality.agreeableness), GROUP_CONCAT(Personality.emotional_stability), GROUP_CONCAT(Personality.conscientiousness), \
                GROUP_CONCAT(Personality.extraversion), \
                GROUP_CONCAT(Metrics.metric), GROUP_CONCAT(Conditions.Condition) \
                FROM Personality \
                INNER JOIN RatingsForPersonality ON RatingsForPersonality.userId = Personality.userId\
                INNER JOIN Metrics ON Metrics.metricId = Personality.`assigned metric` \
                INNER JOIN Conditions ON Conditions.conditionId = Personality.`assigned condition` \
                WHERE RatingsForPersonality.movieId = %s AND RatingsForPersonality.rating >= 4;", (movieId,))
    openness = []
    agreeableness = []
    emotional_stability = []
    conscientiousness = []
    extraversion = []
    metric = []
    condition = []
    
    for row in cur:
        openness = list(map(float, row[0].split(",")))
        agreeableness = list(map(float, row[1].split(",")))
        emotional_stability = list(map(float, row[2].split(",")))
        conscientiousness = list(map(float, row[3].split(",")))
        extraversion = list(map(float, row[4].split(",")))
        metric = row[5].split(",")
        condition = row[6].split(",")

    openness = np.median(openness)
    agreeableness = np.median(agreeableness)
    emotional_stability = np.median(emotional_stability)
    conscientiousness = np.median(conscientiousness)
    extraversion = np.median(extraversion)
    metric = statistics.mode(metric)
    condition = statistics.mode(condition)
    
    conn.close()

    return [openness, agreeableness, emotional_stability, conscientiousness, extraversion, metric, condition]  

def person_traits_enjoy_and_personalized():
    # Which personality traits is it easiest to provide movies for which they will enjoy and they feel is personalised?
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT GROUP_CONCAT(Personality.openness), \
                GROUP_CONCAT(Personality.agreeableness), GROUP_CONCAT(Personality.emotional_stability), GROUP_CONCAT(Personality.conscientiousness), GROUP_CONCAT(Personality.extraversion), \
                GROUP_CONCAT(Metrics.metric), GROUP_CONCAT(Conditions.Condition) \
                FROM Personality \
                INNER JOIN `Personality-Predictions` ON `Personality-Predictions`.userId = Personality.userId \
                INNER JOIN Metrics ON Metrics.metricId = Personality.`assigned metric` \
                INNER JOIN Conditions ON Conditions.conditionId = Personality.`assigned condition` \
                WHERE enjoy_watching >= 4 AND is_personalized >= 4;")

    openness = []
    agreeableness = []
    emotional_stability = []
    conscientiousness = []
    extraversion = []
    metric = []
    condition = []

    for row in cur:
        openness = list(map(float, row[0].split(",")))
        agreeableness = list(map(float, row[1].split(",")))
        emotional_stability = list(map(float, row[2].split(",")))
        conscientiousness = list(map(float, row[3].split(",")))
        extraversion = list(map(float, row[4].split(",")))
        metric = row[5].split(",")
        condition = row[6].split(",")
    
    openness = np.median(openness)
    agreeableness = np.median(agreeableness)
    emotional_stability = np.median(emotional_stability)
    conscientiousness = np.median(conscientiousness)
    extraversion = np.median(extraversion)
    metric = statistics.mode(metric)
    condition = statistics.mode(condition)
    
    conn.close()

    return [openness, agreeableness, emotional_stability, conscientiousness, extraversion, metric, condition]

def train_nn():
    if exists('dataset-5.csv'):
        df = pd.read_csv('dataset-5.csv')
        X = df.drop('Rating', axis=1)
        y = df.pop('Rating')

        X = X.drop('Metric', axis=1)
        X = X.drop('Condition', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle = True)
    else:
        X_train, X_test, y_train, y_test = gen_dataset()
    
    nn = MLPRegressor(random_state=1, max_iter=1000).fit(X_train, y_train)
    
    y_pred = nn.predict(X_test)
    score = mean_absolute_error(y_test, y_pred)
    return nn, score

def gen_dataset():
    conn = connect()
    cur = conn.cursor()
    df = pd.DataFrame()
    cur.execute("SELECT RatingsForPersonality.movieId, Personality.openness, \
        Personality.agreeableness, Personality.emotional_stability, Personality.conscientiousness, Personality.extraversion, \
        Personality.`assigned metric`, Personality.`assigned condition`, RatingsForPersonality.rating \
        FROM RatingsForPersonality \
        INNER JOIN Personality ON Personality.userId = RatingsForPersonality.userId;")
    
    for row in cur:
        movieId = int(row[0])
        openness = float(row[1])
        agreeableness = float(row[2])
        emotional_stability = float(row[3])
        conscientiousness = float(row[4])
        extraversion = float(row[5])
        metric = int(row[6])
        condition = int(row[7])
        rating = float(row[8])
        row = pd.Series([movieId, openness, agreeableness, emotional_stability, conscientiousness, extraversion, metric, condition, rating])
        row_df = pd.DataFrame([row])
        df = pd.concat([df, row_df], ignore_index=True)

    conn.close()        
    df.columns = ['Movie', 'Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted', 'Metric', 'Condition', 'Rating']
    
    
    df.to_csv('dataset-5.csv', index=False)
    
    X = df.drop('Rating', axis=1)
    y = df.pop('Rating')
    X = X.drop('Metric', axis=1)
    X = X.drop('Condition', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle = True)

    return X_train, X_test, y_train, y_test
        

def get_film_viewers(movieId):
    conn = connect()
    cur = conn.cursor()
    df = pd.DataFrame()
    cur.execute("SELECT RatingsForPersonality.movieId, Personality.openness, \
                Personality.agreeableness, Personality.emotional_stability, Personality.conscientiousness, Personality.extraversion, \
                Personality.`assigned metric`, Personality.`assigned condition`, RatingsForPersonality.rating \
                FROM RatingsForPersonality \
                INNER JOIN Personality ON Personality.userId = RatingsForPersonality.userId WHERE movieId = %s", (movieId,))

    for row in cur:
        movieId = int(row[0])
        openness = float(row[1])
        agreeableness = float(row[2])
        emotional_stability = float(row[3])
        conscientiousness = float(row[4])
        extraversion = float(row[5])
        metric = int(row[6])
        condition = int(row[7])
        rating = float(row[8])
        row = pd.Series([movieId, openness, agreeableness, emotional_stability, conscientiousness, extraversion, metric, condition, rating])
        row_df = pd.DataFrame([row])
        df = pd.concat([df, row_df], ignore_index=True)

    conn.close()
    df.columns = ['Movie', 'Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted', 'Metric', 'Condition', 'Rating']

    avg_rating = df['Rating'].mean()
    X = df.drop('Rating', axis=1)
    y = df.pop('Rating')
    X = X.drop('Metric', axis=1)
    X = X.drop('Condition', axis=1)
    
    return X, y, avg_rating


@use_case_5.route("/", methods=["GET", "POST"])
def query():
    # Using the trained ML model, can we predict the actual average mean rating?
    data = request.form
    movieId = int(data["movieId"])

    cached_val = cache.get(movieId)
    if cached_val != None:
        return cached_val
    
    # Predicting avg rating based on subset of users
    if exists('nn.joblib'):
        nn = load('nn.joblib')
    else:
        nn, score = train_nn()
        dump(nn, 'nn.joblib')

    X, y, avg_rating = get_film_viewers(movieId)
    y_pred = nn.predict(X)

    predicted_avg = np.mean(y_pred)
    score = mean_absolute_error(y, y_pred)

    # Personality traits of users who enjoyed the movie the most
    person_traits_most_enjoyed = person_traits_agg(movieId)
    # Extra SQL Data Analysis
    easy_to_predict_users_peron_traits = person_traits_enjoy_and_personalized()

    return_val = {
        'avg_rating': avg_rating,
        'predicted_avg': predicted_avg,
        'score': score,
        'person_traits_most_enjoyed': person_traits_most_enjoyed,
        'easy_to_predict_users_peron_traits': easy_to_predict_users_peron_traits
    }
    cache.set(movieId, return_val)
    return return_val

if __name__ == '__main__':
    use_case_5.run(debug = True, port = 5006, host="0.0.0.0")
