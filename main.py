from flask import request, Flask
import json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    pass


if __name__ == "__main__":
    app.run(port=8080)
