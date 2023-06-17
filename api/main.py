from flask import Flask, request, render_template, make_response, session, jsonify
import base64
import pickle
import logging
import json
# import firebase_admin
# from firebase_admin import credentials, auth
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/users.db'  # Update the database URI if needed
db = SQLAlchemy(app)
# Initialize Firebase Admin SDK
#cred = credentials.Certificate(os.environ.get('FIREBASE_KEY'))  # Path to your service account key JSON file
# cred = credentials.Certificate("goftan.json")  # Path to your service account key JSON file
#firebase_admin.initialize_app(cred)

app.debug = True
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.config['DEBUG'] = True
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
))

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    return str('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


users = []

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='Registration successful!')


@app.route("/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify(message='Login successful!')
    else:
        return jsonify(message='Invalid username or password.')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
