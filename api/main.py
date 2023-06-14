from flask import Flask, request, render_template, make_response, session
import base64
import pickle
import logging
import json

app = Flask(__name__, static_url_path='/static', static_folder='static')

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    app.logger.info(request.data.username)

    if 'rememberme' in request.cookies:
        b64=request.cookies.get('rememberme')
        a = pickle.loads(base64.b64decode(b64))
        session['username'] = a.username
        session['loggedin'] = True
        return render_template("loggedin.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Here you should add the logic to check the username and password
            # For example, you can check them against a database
            if username == 'admin' and password == 'password':
                session['username'] = username
                session['loggedin'] = True
                if 'rememberme' in request.form:
                    if request.form['rememberme'] == 'on':
                        u1 = usr(username, password)
                        ser = pickle.dumps(u1)
                        b64 = base64.b64encode(ser)
                        res = make_response(render_template("loggedin.html"))
                        res.set_cookie("rememberme", b64, 60*60*24*15)
                        return res
                else:
                    return render_template("loggedin.html")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
