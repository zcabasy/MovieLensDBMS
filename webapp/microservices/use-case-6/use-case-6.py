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
    pwd = "password"

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

@use_case_6.route("/")
def home():

    return "6"

if __name__ == '__main__':
    use_case_6.run(debug = True, port = 5007, host="0.0.0.0")
