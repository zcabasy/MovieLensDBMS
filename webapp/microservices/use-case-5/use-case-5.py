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

use_case_5 = Flask(__name__)

use_case_5.config['CACHE_TYPE'] = 'SimpleCache'
use_case_5.config['CACHE_DEFAULT_TIMEOUT'] = 300
use_case_5.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(use_case_5)

def connect():
    # f = open("mysql-user-db1.txt")
    # pwd = f.read()
    # f.close()
    pwd = "password"

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


def subset_preds():
    # Using a subset of viewers, what is the average rating predicted for the entire subset
    pass

def person_traits_agg():
    # Return aggregate stats on personality traits of users who gave the film a high rating
    pass

@use_case_5.route("/")
def query():

    pass

if __name__ == '__main__':
    use_case_5.run(debug = True, port = 5006, host="0.0.0.0")
