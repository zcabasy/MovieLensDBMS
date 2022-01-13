from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/use-case-1")
def use_case_1():
    return render_template("use-case-1/use-case-1.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")