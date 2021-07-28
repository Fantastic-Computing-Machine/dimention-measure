from flask import Flask, render_template, redirect, session, request, flash, url_for
import random
import string

import database
import app
import helper
app = user_auth = Flask(__name__)


def index_view():
    print("INDEX-VIEW:", session)
    # session["projectNameList"] = ["asd","qqq"]
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
            # session["live"] = projectName
            print(session)
            return render_template('records.html', projectName=session["live"])

    return render_template('index.html')


def records_view(projectName):
    try:
        if request.method == "POST":
            name = str(request.form['name'])
            length = int(request.form['length'])
            width = int(request.form['width'])
            rate = int(request.form['rate'])
            namearr = request.form.getlist('name')
            lengtharr = request.form.getlist('length')
            widtharr = request.form.getlist('width')
            sqmarr = request.form.getlist('sqm')
            sqftarr = request.form.getlist('sqft')
            ratearr = request.form.getlist('rate')
            sqm = length*width
            sqft = sqm * 10.764

            print(namearr, lengtharr, widtharr, sqmarr, sqftarr, ratearr)
            return render_template('records.html', projectName=projectName, metrics={"name": name, "length": length, "sqm": sqm, "sqft": sqft, "width":
                                                                                         width, "rate": rate})

        else:
            return render_template('records.html', metrics={})

    except Exception as ex:
        print("EXCEPTION OCCURED: \n")
        print(ex)
        return render_template('records.html', metrics={})
