from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/use-case-1.html")
def use_case_1():
    return render_template("use-case-1.html")

@app.route("/use-case-2.html")
def use_case_2():
    return render_template("use-case-2.html")

@app.route("/use-case-3.html")
def use_case_3():
    return render_template("use-case-3.html")

@app.route("/use-case-4.html")
def use_case_4():
    return render_template("use-case-4.html")

@app.route("/use-case-5.html")
def use_case_5():
    return render_template("use-case-5.html")

@app.route("/use-case-6.html")
def use_case_6():
    return render_template("use-case-6.html")

if __name__ == '__main__':
    app.run(debug = True, port = 5001, host="0.0.0.0")
