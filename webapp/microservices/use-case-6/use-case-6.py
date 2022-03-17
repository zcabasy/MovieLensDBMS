from flask import Flask, request
from flask_caching import Cache
import mariadb
import sys
import numpy as np
import pandas as pd
import statistics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from joblib import dump, load
from os.path import exists
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle

use_case_6 = Flask(__name__)

use_case_6.config['CACHE_TYPE'] = 'SimpleCache'
use_case_6.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_6.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_6)

def connect():
    # f = open("mysql-user-db1.txt")
    # pwd = f.read()
    # f.close()
    pwd = "bWsbM/9AK}#-:eeC*b6D/vKzjK%[x`!C"

    try:
        conn = mariadb.connect(
            user="safebrowser",
            password=pwd,
            host="db-6",
            port=3306,
            database="MovieLensDB"
        )
        print("connected 6", flush=True)
        return conn
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def train_models():
    models = {}

    
    if exists('open_model.joblib'):
        open_model = load('open_model.joblib')
        agreeable_model = load('agreeable_model.joblib')
        emotional_model = load('emotional_model.joblib')
        conscientious_model = load('conscientious_model.joblib')
        extraverted_model = load('extraverted_model.joblib')
        
    else:
        training_x, training_y, testing_x, testing_y = gen_datasets()
        
        open_model = GaussianNB().fit(training_x[0], training_y[0])
        agreeable_model = GaussianNB().fit(training_x[1], training_y[1])
        emotional_model = GaussianNB().fit(training_x[2], training_y[2])
        conscientious_model = GaussianNB().fit(training_x[3], training_y[3])
        extraverted_model = GaussianNB().fit(training_x[4], training_y[4])

        dump(open_model, 'open_model.joblib')
        dump(agreeable_model, 'agreeable_model.joblib')
        dump(emotional_model, 'emotional_model.joblib')
        dump(conscientious_model, 'conscientious_model.joblib')
        dump(extraverted_model, 'extraverted_model.joblib')

        accuracy_open = accuracy_score(testing_y[0], open_model.predict(testing_x[0]))
        accuracy_agreeable = accuracy_score(testing_y[1], agreeable_model.predict(testing_x[1]))
        accuracy_emotional = accuracy_score(testing_y[2], emotional_model.predict(testing_x[2]))
        accuracy_conscientious = accuracy_score(testing_y[3], conscientious_model.predict(testing_x[3]))
        accuracy_extraverted = accuracy_score(testing_y[4], extraverted_model.predict(testing_x[4]))
    
    models["openness"] = open_model
    models["agreeable"] = agreeable_model
    models["emotional"] = emotional_model
    models["conscientious"] = conscientious_model
    models["extraverted"] = extraverted_model
    
    return models

def gen_datasets():
    if exists('dataset-6.csv'):
        df = pd.read_csv('dataset-6.csv')
    else:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT GROUP_CONCAT(DISTINCT Tags.tag), AVG(Personality.openness), \
                    AVG(Personality.agreeableness), AVG(Personality.emotional_stability), AVG(Personality.conscientiousness), AVG(Personality.extraversion) \
                    FROM RatingsForPersonality \
                    INNER JOIN Personality ON Personality.userId = RatingsForPersonality.userId \
                    INNER JOIN Tags ON Tags.movieId = RatingsForPersonality.movieId \
                    WHERE rating >= 4 \
                    GROUP BY RatingsForPersonality.movieId;")
        
        df = pd.DataFrame()
        
        for row in cur:
            tags = row[0]
            openness = float(row[1])
            agreeableness = float(row[2])
            emotional = float(row[3])
            conscientious = float(row[4])
            extraversion = float(row[5])
            row = pd.Series([tags, openness, agreeableness, emotional, conscientious, extraversion])
            row_df = pd.DataFrame([row])
            df = pd.concat([df, row_df], ignore_index=True)

        conn.close()        
        df.columns = ['Tags', 'Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted']
        
        df['Open'] = df['Open'] > 3.5
        
        df['Agreeable'] = df['Agreeable'] > 3.5
        
        df['Emotional'] = df['Emotional'] > 3.5
        
        df['Conscientious'] = df['Conscientious'] > 3.5
        
        df['Extraverted'] = df['Extraverted'] > 3.5
        

        df['Open'].replace(True, 1, inplace=True)
        df['Open'].replace(False, 0, inplace=True)
        df['Agreeable'].replace(True, 1, inplace=True)
        df['Agreeable'].replace(False, 0, inplace=True)
        df['Emotional'].replace(True, 1, inplace=True)
        df['Emotional'].replace(False, 0, inplace=True)
        df['Conscientious'].replace(True, 1, inplace=True)
        df['Conscientious'].replace(False, 0, inplace=True)
        df['Extraverted'].replace(True, 1, inplace=True)
        df['Extraverted'].replace(False, 0, inplace=True)
        
        df.to_csv('dataset-6.csv', index=False)
        
    
    X = df.drop(['Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted'], axis=1)
    
    corpus = []
    for i in range(0, len(X)):
        tag = re.sub('[^a-zA-Z0-9]', ' ', X['Tags'][i])
        tag = tag.lower()
        tag = tag.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        tag = [ps.stem(word) for word in tag if not word in set(all_stopwords)]
        tag = ' '.join(tag)
        corpus.append(tag)
    
    with open("corpus", "wb") as fp:
        pickle.dump(corpus, fp)
    
    cv = CountVectorizer()
    X = cv.fit_transform(corpus).toarray()

    dump(cv, 'cv.joblib')
    
    y_open = df.pop('Open')
    y_agreeable = df.pop('Agreeable')
    y_emotional = df.pop('Emotional')
    y_conscientious = df.pop('Conscientious')
    y_extraverted = df.pop('Extraverted')
    
    X_train_open, X_test_open, y_train_open, y_test_open = train_test_split(X, y_open, test_size=0.3, random_state=42, shuffle = True)
    X_train_agreeable, X_test_agreeable, y_train_agreeable, y_test_agreeable = train_test_split(X, y_agreeable, test_size=0.3, random_state=42, shuffle = True)
    X_train_emotional, X_test_emotional, y_train_emotional, y_test_emotional = train_test_split(X, y_emotional, test_size=0.3, random_state=42, shuffle = True)
    X_train_conscientious, X_test_conscientious, y_train_conscientious, y_test_conscientious = train_test_split(X, y_conscientious, test_size=0.3, random_state=42, shuffle = True)
    X_train_extraverted, X_test_extraverted, y_train_extraverted, y_test_extraverted = train_test_split(X, y_extraverted, test_size=0.3, random_state=42, shuffle = True)

    training_x = [X_train_open, X_train_agreeable, X_train_emotional, X_train_conscientious, X_train_extraverted]
    training_y = [y_train_open, y_train_agreeable, y_train_emotional, y_train_conscientious, y_train_extraverted]
    testing_x = [X_test_open, X_test_agreeable, X_test_emotional, X_test_conscientious, X_test_extraverted]
    testing_y = [y_test_open, y_test_agreeable, y_test_emotional, y_test_conscientious, y_test_extraverted]
    
    return training_x, training_y, testing_x, testing_y

def movie_data(movieId):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT GROUP_CONCAT(DISTINCT Tags.tag), AVG(Personality.openness), \
                AVG(Personality.agreeableness), AVG(Personality.emotional_stability), AVG(Personality.conscientiousness), AVG(Personality.extraversion) \
                FROM RatingsForPersonality \
                INNER JOIN Personality ON Personality.userId = RatingsForPersonality.userId \
                INNER JOIN Tags ON Tags.movieId = RatingsForPersonality.movieId \
                WHERE rating >= 4 AND RatingsForPersonality.movieId = %s", (movieId,))

    df = pd.DataFrame()
    
    for row in cur:
        tags = row[0]
        openness = float(row[1])
        agreeableness = float(row[2])
        emotional = float(row[3])
        conscientious = float(row[4])
        extraversion = float(row[5])
        row = pd.Series([tags, openness, agreeableness, emotional, conscientious, extraversion])
        row_df = pd.DataFrame([row])
        df = pd.concat([df, row_df], ignore_index=True)

    conn.close()
    
    df.columns = ['Tags', 'Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted']
    y = df.drop(['Tags'], axis=1)
    
    tags = df['Tags']
    
    with open("corpus", "rb") as fp:
        corpus = pickle.load(fp)
    
    for i in range(0, len(df)):
        tag = re.sub('[^a-zA-Z0-9]', ' ', df['Tags'][i])
        tag = tag.lower()
        tag = tag.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        tag = [ps.stem(word) for word in tag if not word in set(all_stopwords)]
        tag = ' '.join(tag)
        corpus.append(tag)
    
    cv = load('cv.joblib')
    df = cv.transform(corpus).toarray()
    df = [df[-1]] #only want df for the movie we want
    return df, tags, y

@use_case_6.route("/", methods=["GET", "POST"])
def query():
    data = request.form
    movieId = int(data["movieId"])

    cached_val = cache.get(movieId)
    if cached_val != None:
        return cached_val
    
    models = train_models()
    movie_tags, tags, y = movie_data(movieId) #Movie_tags is the cv transformed corpus, tags is the original tags, y is the actual personality traits in raw form
    traits = {}
    for key in models:
        prediction = models[key].predict(movie_tags)
        traits[key] = prediction

    return_val = [traits, y, tags]
    cache.set(movieId, return_val)
    return return_val

if __name__ == '__main__':
    use_case_6.run(debug = True, port = 5007, host="0.0.0.0")
