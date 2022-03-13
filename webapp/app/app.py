import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

print("Starting program...")

@app.route("/", methods=["GET", "POST"])
@app.route("/use-case-1.html",  methods=["GET", "POST"])
def use_case_1_run():
    if request.method == "POST":
        req = request.form

        movieTitle = req.get("movieTitle")
        genre = req.get("genre")
        rating = req.get("rating")

        # POST request to microservices (NOT WORKING)
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5002', json=req)
        # print('Response from server: ', res.text)

        # return redirect('http://localhost:5002', query=req)
        # print(use_case_1.query_table(req))

        # return redirect(url_for(use-case-1, query=req) # testing

    return render_template("use-case-1.html")


@app.route("/use-case-2.html",  methods=["GET", "POST"])
def use_case_2_run():
    
    if request.method == "POST":
        req = request.form

        movieName = req.get("movieName")

        # POST request to microservices
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5003/', json=req)
        # print('Response from server: ', res.text)

        # print(req)
    return render_template("use-case-2.html")


@app.route("/use-case-3.html", methods=["GET", "POST"])
def use_case_3_run():
    if request.method == "POST":
        req = request.form

        popularTable = req.get("popularTable")
        unpopularTable = req.get("unpopularTable")

        # POST request to microservices
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5004', json=req)
        # print('Response from server: ', res.text)
        
        # print(req)
    return render_template("use-case-3.html")


@app.route("/use-case-4.html", methods=["GET", "POST"])
def use_case_4_run():
    if request.method == "POST":
        req = request.form

        form4 = req.get("form4")

        # POST request to microservices
        # 1. serialize dict to JSON
        # 2. write correct MIME type ('application/json') in the HTTP header
        # res = requests.post('http://localhost:5005/', json=req)
        # print('Response from server: ', res.text)

    return render_template("use-case-4.html")


@app.route("/use-case-5.html", methods=["GET", "POST"])
def use_case_5_run():
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
def use_case_6_run(): 
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
