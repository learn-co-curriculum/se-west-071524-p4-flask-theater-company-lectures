#!/usr/bin/env python3

# 📚 Review With Students:
# Request-Response Cycle
# Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
# `Flask` from `flask`
# `Migrate` from `flask_migrate`
# db and `Production` from `models`
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from models import Production, db

# 3. ✅ Initialize the App
# Add `app = Flask(__name__)`
app = Flask(__name__)

# Configure the database by adding`app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
# and `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set the migrations with `migrate = Migrate(app, db)`
migrate = Migrate(app, db)

# Finally, initialize the application with `db.init_app(app)`
db.init_app(app)

# 4. ✅ Migrate
# `cd` into the `server` folder

# Run in Terminal
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m 'Create tables productions'
# flask db upgrade


# Review the database to verify your table has migrated correctly

# 5. ✅ Navigate to `seed.rb`


# 12. ✅ Routes
# Create your route
# @app.route("/hello")
# def index():
#     return "<h1>Hello World</h1>"
#     # `@app.route('/')
#     #  def index():
#     #    return '<h1>Hello World!</h1>'`


# 13. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`


@app.route("/productions")
def index():
    productions = Production.query.all()  # READ all productions from productions table
    # import ipdb

    # ipdb.set_trace()
    prods_dict = [
        {
            "title": production.title,
            "genre": production.genre,
            "director": production.director,
        }
        for production in productions
    ]
    return jsonify(prods_dict), 200


# 14. ✅ Create a dynamic route
# `@app.route('/productions/<string:title>')
#  def production(title):
#     return f'<h1>{title}</h1>'`
# @app.route("/productions/<string:title>")
# def production(title):
#     return f"<h2>We are proud to present {title.upper()}</h2>"


# 15.✅ Update the route to find a `production` by its `title` and send it to our browser

# Before continuing, import `jsonify` and `make_response` from Flask at the top of the file.

# 📚 Review With Students: status codes
# `make_response` will allow us to make a response object with the response body and status code
# `jsonify` will convert our query into JSON

# `@app.route('/productions/<string:title>')
# def production(title):
#     production = Production.query.filter(Production.title == title).first()
#     production_response = {
#         "title":production.title,
#         "genre":production.genre,
#         "director": production.director
#         }
#     response = make_response(
#         jsonify(production_response),
#         200
#     )`


@app.route("/productions/<int:id>", methods=["GET"])
def show(id):
    production = Production.query.get(id)
    try:
        prod_dict = {
            "title": production.title,
            "genre": production.genre,
            "director": production.director,
        }
        return make_response(
            prod_dict, 200
        )  # make_respones will call jsonify on your dictionary
    except:
        prod_dict = {"error": f"No prodction found with the id: {id}"}
        return make_response(prod_dict, 404)


@app.route("/productions/<string:title>")
def production_by_title(title):
    production = Production.query.filter(Production.title == title.title()).first()
    try:
        prod_dict = {
            "title": production.title,
            "genre": production.genre,
            "director": production.director,
        }
        return make_response(
            prod_dict, 200
        )  # make_respones will call jsonify on your dictionary
    except:
        prod_dict = {"error": f"No prodction found with the title: {title.title()}"}
        return make_response(prod_dict, 404)


# 16.✅ View the path and host with request context
@app.route("/context")
def context():
    return (
        f"<h1>Path: {request.path} Host: {request.host} Method: {request.method}</h1>"
    )


# 17.✅ Use the before_request request hook, what this hook does is up to you. You could hit a breakpoint, print something to server console or anything else you can think of.
@app.before_request
def runs_before():
    current_user = {"user_id": 1, "username": "Skyler"}
    print(current_user)


# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below
# and run `python app.py`

if __name__ == "__main__":
    app.run(port=5555, debug=True)
