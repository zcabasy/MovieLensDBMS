from curses import meta
from urllib import request
from flask import Flask
from flask_caching import Cache
import mariadb
import sys

data_catalogue = Flask(__name__)

cache = Cache()
cache.init_app(data_catalogue)
data_catalogue.config['CACHE_TYPE'] = 'SimpleCache'


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

@data_catalogue.route("/",  methods=["GET", "POST"])
def query_table():

        sql= "SELECT * FROM information_schema.tables WHERE table_schema='MovieLensDB'\G" # alternative test code to view information schema 

        conn = connect()
        cur = conn.cursor()
        cur.execute(sql) 
        
        # Parse response and package into something that can be returned e.g. JSON
        response = ""

        conn.close()
        
        return response

if __name__ == '__main__':
    data_catalogue.run(debug = True, port = 5010, host="0.0.0.0")
