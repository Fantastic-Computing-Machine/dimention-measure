from flask import Flask, session, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

from views import index_view, records_view, delete_view, deleteProject_view
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
    if projectName in session["projectNameList"]:
        return records_view(projectName)
    return render_template("error_404.html")


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
    sessionlist = session['projectNameList']
    sessionlist.remove(projectName)
    session['projectNameList'] = sessionlist
    return deleteProject_view(projectName)


@app.errorhandler(404)
def not_found(e):
    return render_template("error_404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
