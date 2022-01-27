from flask import Flask

use_case_2 = Flask(__name__)

@use_case_2.route("/")
def home():
    return "2"

if __name__ == '__main__':
    use_case_2.run(debug = True, port = 5003, host="0.0.0.0")