from flask import Flask, session
from flask.helpers import url_for
from werkzeug.utils import redirect

from views import index_view, records_view, error_404_view, delete_view, deleteProject_view
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


@app.route('/delete/<projectName>/<rowNumber>/', methods=["POST", "GET"])
def delete(projectName, rowNumber):
    helper.initialization()
    return delete_view(projectName, rowNumber)


@app.route('/success/<projectName>/', methods=["POST", "GET"])
def success(projectName):
    print("success")
    return redirect(url_for('record', projectName=projectName))


@app.route('/delete/<projectName>/', methods=["POST", "GET"])
def deleteProject(projectName):
    return deleteProject_view(projectName)


@app.route('/error_404/')
def error_404():
    return error_404_view()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
