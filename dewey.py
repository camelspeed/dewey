from flask import Flask, abort
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Dr. Falken! Do you want to play a game?"

@app.route("/<name>")
def greeting(name):
    return 'Hello %s! Do you want to play a game?' % name

@app.route("/401")
def error401():
    abort(401)

@app.route("/404")
def error404():
    abort(404)

@app.route("/500")
def error500():
    abort(500)

if __name__ == "__main__":
    app.debug = True
    app.run()
