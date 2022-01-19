from flask import Flask

use_case_4 = Flask(__name__)

@use_case_4.route("/")
def home():
    return "4"

if __name__ == '__main__':
    use_case_4.run(debug = True, port = 5005, host="0.0.0.0")