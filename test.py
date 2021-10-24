from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome Mediapipe"

@app.route('/route1')
def route1():
    return "This executed from route1 function"

def route2():
    return "This executed from route2 function"

app.add_url_rule('/route2', 'route2', route2)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)