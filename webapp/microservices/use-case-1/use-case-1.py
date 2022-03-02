from flask import Flask
from flask_caching import Cache

use_case_1 = Flask(__name__)

cache = Cache()
cache.init_app(use_case_1)
use_case_1.config['CACHE_TYPE'] = 'SimpleCache'

@use_case_1.route("/")
#should add max memory size to this
#limited timeout to ensure we don't run out of memory
#we have in memory and in process caching here
#should we use out of process caching if we want to spin up multiple instance of each microservice? -> no, out of scope for this project
@cache.memoize(timeout=60)
def home():
    return "1"

if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")