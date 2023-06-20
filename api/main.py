from flask import Flask, request, render_template, make_response, session
import base64
import pickle
import logging
import json
from flask import request
import os
from flask_socketio import SocketIO 
from flask_socketio import emit


app = Flask(__name__, static_url_path='/static', static_folder='static')
socketio = SocketIO()

# Initialize Firebase Admin SDK
#cred = credentials.Certificate(os.environ.get('FIREBASE_KEY'))  # Path to your service account key JSON file
# cred = credentials.Certificate("goftan.json")  # Path to your service account key JSON file
# firebase_admin.initialize_app(cred)
#yag = yagmail.SMTP('divlengua@gmail.com', 'DivLenguaLanguageLearningApp0')  # Replace with your Gmail email address and password
# yag = yagmail.SMTP("divlengua@gmail.com", oauth2_file="client.json")
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

class usr:
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def start():
    return render_template("index.html")

# def send_confirmation_email(email):
#     logging.info("email looks to be sent."+ email)
#     try:
#         # user = auth.get_user_by_email(email)

#         # Generate the email verification link
#         # email_verification_link = auth.generate_email_verification_link(email)

#         subject = 'Confirmation Email'
#         message = f'Click the following link to confirm your email: {email_verification_link}'

#         # yag.send(to=email, subject=subject, contents=message)
#         logging.info("email looks to be sent.")
#         return 'Confirmation email sent successfully!'
#     except:
#         return 'Error sending confirmation email'

@app.route("/register", methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # send_confirmation_email(username)

    try:
        
        # user = auth.create_user(
        #     email=username,
        #     password=password
        # )
        # email_link = auth.generate_email_verification_link(username)
        # User registration successful
        # You can perform additional actions or return a response indicating successful registration
        return 'Registered successfully!'
    except:
        # Registration error
        # Handle the error appropriately
        return 'Registration failed!'

@app.route("/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        # user = auth.get_user_by_email(username)
        # User exists, proceed with authentication
        # Use Firebase Admin SDK to verify the password or perform other checks
        # If authentication is successful, return a response indicating successful login
        # Otherwise, handle the authentication failure
        return 'Logged in successfully!'
    except:
        # User not found or other authentication error
        # Handle the error appropriately
        return 'Authentication failed!'
    # app.logger.info(request.data.username)
    # app.logger.info(username)
    # app.logger.info(password)
    # if 'rememberme' in request.cookies:
    #     b64=request.cookies.get('rememberme')
    #     a = pickle.loads(base64.b64decode(b64))
    #     session['username'] = a.username
    #     session['loggedin'] = True
    #     return render_template("loggedin.html")
    # else:
        
    #     if request.method == 'POST':
    #         data = request.get_json()
    #         username = data.get('username')
    #         password = data.get('password')
    
    #         # Here you should add the logic to check the username and password
    #         # For example, you can check them against a database
    #         if username == 'admin' and password == 'password':
    #             session['username'] = username
    #             session['loggedin'] = True
    #             if 'rememberme' in request.form:
    #                 if request.form['rememberme'] == 'on':
    #                     u1 = usr(username, password)
    #                     ser = pickle.dumps(u1)
    #                     b64 = base64.b64encode(ser)
    #                     res = make_response(render_template("loggedin.html"))
    #                     res.set_cookie("rememberme", b64, 60*60*24*15)
    #                     return res
    #             else:
    #                 return render_template("loggedin.html")
    return render_template("index.html")

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)

socketio.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
