from flask import Flask

use_case_1 = Flask(__name__)

@use_case_1.route("/")
def home():
    return "1"

if __name__ == '__main__':
    use_case_1.run(debug = True, port = 5002, host="0.0.0.0")