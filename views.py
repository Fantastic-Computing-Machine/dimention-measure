from flask import Flask, render_template, redirect, session, request,flash,url_for
import random
import string

import database
import app
import helper
app = user_auth = Flask(__name__)


def index_view():
    print("INDEX-VIEW:", session)
    session["projectNameList"] = ["asd","qqq"]
    if request.method == "POST":
        projectName = str(request.form['new_project_name']).replace(" ", "-")
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
    try:
        if request.method == "POST":
            name = str(request.form['name'])
            length = int(request.form['length'])
            width = int(request.form['width'])
            rate = int(request.form['rate'])

            sqm = length*width
            sqft = sqm * 10.764

            print(name, length, width, rate, sqm, sqft)
            return render_template('records.html', metrics={"name": name, "length": length, "sqm": sqm, "sqft": sqft, "width":
                                                            width, "rate": rate})

        else:
            return render_template('records.html', metrics={})

    except Exception as ex:
        print("EXCEPTION OCCURED: \n")
        print(ex)
        return render_template('records.html', metrics={})
