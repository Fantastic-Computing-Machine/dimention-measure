from flask import Flask, session, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from views import index_view, records_view, delete_view, deleteProject_view
from views import download_excel_view

from expense_urls import expense_urls
import helper

from CONFIG import SECRET_KEY, DATABASE_URI


app = Flask(__name__)

app.register_blueprint(expense_urls, url_prefix="/expense/")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
# app.secret_key = SECRET_KEY


@app.route('/', methods=["POST", "GET"])
def index():
    # Homepage
    if request.method == "GET":
        ip_address = request.remote_addr
        print("Current IP: ", ip_address)
        helper.initialization()
    return index_view()


@app.route('/record/<string:projectName>/<int:pid>', methods=["POST", "GET"])
def record(projectName, pid):
    if("projectNameList" not in session):
        helper.initialization()
    if projectName in session["projectNameList"]:
        return records_view(projectName, pid)
    return render_template("error_404.html")


@app.route('/delete/<string:projectName>/<int:pid>/<rowNumber>/', methods=["POST", "GET"])
def delete(projectName, pid, rowNumber):
    return delete_view(projectName, pid, rowNumber)


@app.route('/success/<string:projectName>/<int:pid>', methods=["POST", "GET"])
def success(projectName, pid):
    print("success")
    return redirect(url_for('record', projectName=projectName, pid=pid))


@app.route('/delete/<projectName>/', methods=["POST", "GET"])
def deleteProject(projectName):
    return deleteProject_view(projectName)


@app.route('/download_excel/<projectName>/', methods=["POST", "GET"])
def download_excel(projectName):
    # route to download to excel
    print("Downloades-->", projectName)
    return download_excel_view(projectName)


@app.errorhandler(404)
def not_found(e):
    return render_template("error_404.html")


if __name__ == "__main__":
    # app.init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)