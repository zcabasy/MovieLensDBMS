from flask import Flask, render_template, request

app = Flask(__name__)

print("Starting program...")
@app.route("/", methods=["GET", "POST"])
@app.route("/use-case-1.html",  methods=["GET", "POST"])
def use_case_1():
    if request.method == "POST":
        req = request.form

        movieTitle = req.get("movieTitle")
        genre = req.get("genre")
        rating = req.get("rating")
        # print(req)

    return render_template("use-case-1.html")


@app.route("/use-case-2.html",  methods=["GET", "POST"])
def use_case_2():
    if request.method == "POST":
        req = request.form

        movieName = req.get("movieName")

        # print(req)
    return render_template("use-case-2.html")


@app.route("/use-case-3.html", methods=["GET", "POST"])
def use_case_3():
    if request.method == "POST":
        req = request.form

        popularTable = req.get("popularTable")
        unpopularTable = req.get("unpopularTable")
        
        # print(req)
    return render_template("use-case-3.html")


@app.route("/use-case-4.html", methods=["GET", "POST"])
def use_case_4():
    if request.method == "POST":
        req = request.form

        form4 = req.get("form4")
    return render_template("use-case-4.html")


@app.route("/use-case-5.html", methods=["GET", "POST"])
def use_case_5():
    if request.method == "POST":
        req = request.form

        form5 = req.get("form5") 
    return render_template("use-case-5.html")


@app.route("/use-case-6.html", methods=["GET", "POST"])
def use_case_6(): 
    if request.method == "POST":
        req = request.form

        form6 = req.get("form6")
    return render_template("use-case-6.html")

if __name__ == '__main__':
    app.run(debug = True, port = 5001, host="0.0.0.0")
