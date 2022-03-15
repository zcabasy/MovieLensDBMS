from ast import Pass
import requests
from flask import Flask, render_template, request
from flask_caching import Cache

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_THRESHOLD'] = 500
cache = Cache()
cache.init_app(app)

@app.route("/", methods=["GET", "POST"])
# @cache.cached(timeout=300)
@app.route("/use-case-1.html",  methods=["GET", "POST"])
# @cache.cached(timeout=300)
def use_case_1():
    if request.method == "POST":
        # req = request.form

        # movieTitle = req.get("movieTitle")
        # genre = req.get("genre")
        # rating = req.get("rating")

        movieTitle = "toy story"
        genre = "adventure,action"
        min_rating = 0
        max_rating = 5
        tag = "adventure,action"
        sort_by = "title ASC"
        
        form_data = {'title': movieTitle, 
                    'genre': genre,
                    'tag': tag,
                    'min_rating': min_rating, 
                    'max_rating': max_rating, 
                    'sort_by': sort_by}

        response = requests.post('http://use-case-1:5002/', form_data)
        #render response in web page

    return render_template("use-case-1.html")


@app.route("/use-case-2.html",  methods=["GET", "POST"])
def use_case_2():
    
    if request.method == "POST":
        # req = request.form

        # movieName = req.get("movieName")

        movieId = 1
        form_data = {'movieId': movieId}

        response = requests.post('http://use-case-2:5003/', form_data)
        #render response

    return render_template("use-case-2.html")


@app.route("/use-case-3.html", methods=["GET", "POST"])
def use_case_3():
    if request.method == "POST":
        response = requests.post('http://use-case-3:5004/')
        #render response

    return render_template("use-case-3.html")


@app.route("/use-case-4.html", methods=["GET", "POST"])
def use_case_4():
    if request.method == "POST":
        req = request.form

        form4 = req.get("form4")

        movieId = 1
        form_data = {'movieId': movieId}

        response = requests.post('http://use-case-4:5005/', form_data)
        #render response

    return render_template("use-case-4.html")


@app.route("/use-case-5.html", methods=["GET", "POST"])
def use_case_5():
    if request.method == "POST":
        req = request.form

        form5 = req.get("form5") 

        # POST request to microservices
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5006/', json=req)
        # print('Response from server: ', res.text)

    return render_template("use-case-5.html")


@app.route("/use-case-6.html", methods=["GET", "POST"])
def use_case_6(): 
    if request.method == "POST":
        req = request.form

        form6 = req.get("form6")

        # POST request to microservices
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5007/', json=req)
        # print('Response from server: ', res.text)

    return render_template("use-case-6.html")

if __name__ == '__main__':
    app.run(debug = True, port = 5001, host="0.0.0.0")
