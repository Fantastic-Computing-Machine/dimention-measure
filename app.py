from flask import Flask, session
from werkzeug.utils import redirect

from views import index_view, records_view, error_404_view
import helper

app = Flask(__name__)

app.secret_key = "fantasticcomputingmachine"


@app.route('/', methods=["POST", "GET"])
def index():
    # Homepage
    helper.initialization()
    return index_view()


@app.route('/record/<projectName>/', methods=["POST", "GET"])
def record(projectName):
    helper.initialization()
    return records_view(projectName)


@app.route('/error_404/')
def error_404():
    return error_404_view()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
