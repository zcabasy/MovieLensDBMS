from flask import Flask, request

use_case_5 = Flask(__name__)

@use_case_5.route("/")
def home():
    query = request.form
    #movieId = query.get("movieId")
    print("Post received, " + request +
          " sent to Microservices 5", flush=True)

    return "5"

if __name__ == '__main__':
    use_case_5.run(debug = True, port = 5006, host="0.0.0.0")
