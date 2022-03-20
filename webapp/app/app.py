from ast import Pass
from re import T
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
import html


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
    if request.method == "GET":
        response = requests.get("http://use-case-1:5002/")
        genres = response.json()['genres']
        if 'error' in request.args:
            return render_template("use-case-1.html", genres=genres, error=True)
        return render_template("use-case-1.html", genres=genres)

    elif request.method == "POST":
        req = request.form
        movieTitle = sanitize(req.get("movieTitle"))

        genre = ','.join(req.getlist("genre"))
        min_rating = req.get("min_rating")
        max_rating = req.get("max_rating")
        tag = sanitize(req.get("tags"))
        sort_by = req.get("sort_by") 
        
        # dummy data
        # movieTitle = "toy story 2"; genre = "adventure"; min_rating = 0;
        # max_rating = 5; tag = "animation"; sort_by = "title ASC";
        
        form_data = {
            'title': movieTitle, 
            'genre': genre,
            'tag': tag,
            'min_rating': min_rating, 
            'max_rating': max_rating, 
            'sort_by': sort_by
        }
        response = requests.post('http://use-case-1:5002/', form_data)
        try:
            movies = response.json()['movies']
        except:
            return redirect(url_for('use_case_1', error=True), code=302)
        if len(movies) < 1:
            return redirect(url_for('use_case_1', error=True), code=302)
        
    return render_template("use-case-1.html", movies=movies)


@app.route("/use-case-2.html",  methods=["GET", "POST"])
def use_case_2():
    
    if request.method == "POST":
        # req = request.form

        # movieSearch = req.get("movieSearch")

        movieId = 1
        form_data = {'movieId': movieId}

        response = requests.post('http://use-case-2:5003/', form_data)
        data = response.json()
    return render_template("use-case-2.html", data=data)


@app.route("/use-case-3.html", methods=["GET", "POST"])
def use_case_3():
    response = requests.get('http://use-case-3:5004/')
    popular_genres = response.json()['popular_genres']
    polarising_genres = response.json()['polarising_genres']

    return render_template("use-case-3.html",
                           popular_genres=popular_genres,
                           polarising_genres=polarising_genres)


@app.route("/use-case-4.html", methods=["GET", "POST"])
def use_case_4():
    if request.method == "POST":
        req = request.form
        movieId = 1 # req.get("movieId")
        form_data = {'movieId': movieId}
        response = requests.post('http://use-case-4:5005/', form_data)
        score = response.json()['score']
        y_test = response.json()['y_test']
        y_pred = response.json()['y_pred']
        subset_stats = response.json()['subset_stats']
        full_stats = response.json()['full_stats']
        return render_template("use-case-4.html",
                               movieId=movieId,
                               score=score,
                               y_test=y_test,
                               y_pred=y_pred,
                               subset_stats=subset_stats,
                               full_stats=full_stats)
    return render_template("use-case-4.html")


@app.route("/use-case-5.html", methods=["GET", "POST"])
def use_case_5():
    if request.method == "POST":
        req = request.form
        movieId = 1 # req.get("movieId")
        form_data = {'movieId': movieId}
        response = requests.post('http://use-case-5:5006/', form_data)
        avg_rating = response.json()['avg_rating']
        predicted_avg = response.json()['predicted_avg']
        score = response.json()['score']
        person_traits_most_enjoyed = response.json()['person_traits_most_enjoyed']
        easy_to_predict_users_peron_traits = response.json()['easy_to_predict_users_peron_traits']
        return render_template("use-case-5.html",
                               movieId=movieId,
                               avg_rating=avg_rating,
                               predicted_avg=predicted_avg,
                               score=score,
                               person_traits_most_enjoyed=person_traits_most_enjoyed,
                               easy_to_predict_users_peron_traits=easy_to_predict_users_peron_traits)
        
    return render_template("use-case-5.html")


@app.route("/use-case-6.html", methods=["GET", "POST"])
def use_case_6(): 
    if request.method == "POST":
        req = request.form
        movieId = 1 # req.get("movieId")
        form_data = {'movieId': movieId}

        response = requests.post('http://use-case-6:5007/', form_data)
        # traits is a dict with keys: 'openness', 'agreeable', 'emotional', 'conscientious', 'extraverted'
        traits = response.json()['traits']
        # y is a dict witk keys: 'Open', 'Agreeable', 'Emotional', 'Conscientious', 'Extraverted'
        y = response.json()['y']
        # tags is a list of strings
        tags = response.json()['tags']
        return render_template("use-case-6.html",
                               movieId=movieId,
                               traits=traits,
                               y=y,
                               tags=tags)


    return render_template("use-case-6.html")

def sanitize(data):
    output = html.escape(data)

    # blacklisted keys that could be used for sql injection
    punc = '''-;\%*_'''
    for ele in output:
        if ele in punc:
            output = output.replace(ele, "")
    return output

if __name__ == '__main__':
    app.run(debug = True, port = 5001, host="0.0.0.0")
