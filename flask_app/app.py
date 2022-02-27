from flask import Flask, session, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from views import index_view, records_view, delete_view, deleteProject_view
from views import download_excel_view, update_dimention_view

from expense_urls import expense_urls
import helper

from CONFIG import SECRET_KEY, DATABASE_URI


app = Flask(__name__)

app.register_blueprint(expense_urls, url_prefix="/expense/")

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


@app.route('/<string:projectName>/record/<int:pid>', methods=["POST", "GET"])
def record(projectName, pid):
    if("projectNameList" not in session):
        helper.initialization()
    if projectName in session["projectNameList"]:
        return records_view(projectName, pid)
    return render_template("error_404.html")


@app.route('/<string:projectName>/delete/<int:pid>_<int:dimid>/', methods=["POST", "GET"])
def delete(projectName, pid, dimid):
    return delete_view(projectName, pid, dimid)


@app.route('/<string:projectName>/success/<int:pid>', methods=["POST", "GET"])
def success(projectName, pid):
    print("success")
    return redirect(url_for('record', projectName=projectName, pid=pid))


@app.route('/<string:projectName>/delete/', methods=["POST", "GET"])
def deleteProject(projectName):
    return deleteProject_view(projectName)


@app.route('/<string:projectName>/download_excel/', methods=["POST", "GET"])
def download_excel(projectName):
    # route to download to excel
    print("Downloads-->", projectName)
    return download_excel_view(projectName)


@app.route('/<string:projectName>/update/<int:pid>_<int:dimid>/', methods=["POST", "GET"])
def update_dimention(projectName, pid, dimid):
    return update_dimention_view(projectName, pid, dimid)


@app.errorhandler(404)
def not_found(e):
    return render_template("error_404.html")


if __name__ == "__main__":
    # app.init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)
