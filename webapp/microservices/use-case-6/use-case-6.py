from flask import Flask, request

use_case_6 = Flask(__name__)

@use_case_6.route("/")
def home():

    query = request.form
    print("Post received, " + query +
          " sent to Microservices 6", flush=True)

    return "6"

if __name__ == '__main__':
    use_case_6.run(debug = True, port = 5007, host="0.0.0.0")
