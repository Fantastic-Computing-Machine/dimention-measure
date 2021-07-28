from flask import Flask, render_template, redirect, session, request, flash, url_for
import random
import string

import database
import app


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
            return render_template('records.html', projectName=projectName)

    return render_template('index.html')


def records_view(projectName):
    try:
        md = database.MongoDatabase()
        mdb = database.MongoDocumentCreator()
        result = md.findOne({"projectName": projectName})["dims"]
        if request.method == "POST":
            name = str(request.form['name'])
            length = float(int(request.form['length']))
            width = float(int(request.form['width']))
            rate = float(int(request.form['rate']))
            sqm = round(length*width, 2)
            sqft = round(sqm * 10.764, 2)
            print(result)

            dimentions = mdb.dimsCreator(len(result), name, length, width, sqm, sqft, rate)
            
            print(dimentions)
            return render_template('records.html', dims=result, projectName=projectName)

        else:
            return render_template('records.html',dims=result)

    except Exception as ex:
        print("EXCEPTION OCCURED: \n")
        print(ex)
        return render_template('records.html',dims=result)
