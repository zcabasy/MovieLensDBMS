from flask import Flask

use_case_3 = Flask(__name__)

@use_case_3.route("/")
def home():
    return "3"

if __name__ == '__main__':
    use_case_3.run(debug = True, port = 5004, host="0.0.0.0")