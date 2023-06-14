from flask import Flask, request, render_template, make_response, session
import base64
import pickle

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = False
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
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
