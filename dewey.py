from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Dr. Falken! Do you want to play a game?"

@app.route("/<name>")
def greeting(name):
    return 'Hello %s! Do you want to play a game?' % name

if __name__ == "__main__":
    app.debug = True
    app.run()
