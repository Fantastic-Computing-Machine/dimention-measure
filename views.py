from flask import Flask, render_template, redirect, session, request,flash,url_for
import random
import string

import database
import app
import helper
import database
app = user_auth = Flask(__name__)


def index_view():
    print("INDEX-VIEW:", session)
    session["projectNameList"] = ["asd","qqq"]
    if request.method == "POST":
        projectName = request.form.get("projectName")
        print(projectName)
        if projectName in session["projectNameList"]:
            flash("Project name already exists! Please try with different name :)")
            return redirect(request.url)
        else:
            md = database.MongoDatabase()
            mdb = database.MongoDocumentCreator()
            try:
                md.postQuery(mdb.projectInitialization(projectName))
            except Exception as e:
                print(e)
                # add 404 page
            session["projectNameList"].append(str(projectName))
            return redirect(url_for('record',projectName=projectName))
    return render_template('index.html')


def records_view(projectName):
    
    return render_template('records.html')
