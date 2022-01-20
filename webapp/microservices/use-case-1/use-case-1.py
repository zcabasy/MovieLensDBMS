from flask import Flask
from flask_caching import Cache

use_case_1 = Flask(__name__)

cache = Cache()
cache.init_app(use_case_1)
use_case_1.config['CACHE_TYPE'] = 'memcached'

@use_case_1.route("/")
@cache.memoize(timeout=60)
def home():
    return "1"

if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")