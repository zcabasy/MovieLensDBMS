from flask import Flask

use_case_5 = Flask(__name__)

@use_case_5.route("/")
def home():
    return "5"

if __name__ == '__main__':
    use_case_5.run(debug = True, port = 5006, host="0.0.0.0")