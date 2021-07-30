from flask import Flask, render_template, redirect, session, request, flash, url_for
from pymongo.message import query

import database
import app


app = Flask(__name__)


def index_view():
    if request.method == "POST":
        projectName = str(request.form['new_project_name']).replace(" ", "-")
        print("ProjectName->", projectName)
        if projectName in session["projectNameList"]:
            flash("Project name already exists! Please try with different name :)")
            return redirect(request.url)
        else:
            md = database.MongoDatabase()
            mdb = database.MongoDocumentCreator()
            try:
                md.postQuery(mdb.projectInitialization(projectName))
                sessionlist = session['projectNameList']
                sessionlist.append(projectName)

                session['projectNameList'] = sessionlist

            except Exception as e:
                print(e)
            return redirect(url_for('record', projectName=projectName))

    return render_template('index.html')


def records_view(projectName):
    try:
        md = database.MongoDatabase()
        mdb = database.MongoDocumentCreator()

        project_json = md.findOne({"projectName": projectName})
        project_dimentions = project_json["dims"]

        sum_sqm = 0
        sum_sqft = 0
        for _ in project_dimentions:
            sum_sqm = sum_sqm + _["sqm"]
            sum_sqft = sum_sqft + _["sqft"]

        if request.method == "POST":
            name = str(request.form['name'])
            length = float(int(request.form['length']))
            width = float(int(request.form['width']))
            rate = float(int(request.form['rate']))

            sqm = round(length*width, 2)
            sqft = round(sqm * 10.764, 2)

            max = 0
            for i in project_dimentions:
                if(i['dimId'] >= max):
                    max = i['dimId']

            new_dimentions = mdb.dimsCreator(
                max+1, name, length, width, sqm, sqft, rate)

            project_dimentions.append(new_dimentions)
            print(project_dimentions)
            query = {"projectName": projectName}
            update = md.updateData(query, "$set", {"dims": project_dimentions})

            print("Update-Status", update)

            new_dimentions = None
            return redirect(url_for('success', projectName=projectName))
        else:
            return render_template('records.html', project_json=project_dimentions, projectName=projectName, sum_sqm=round(sum_sqm, 2), sum_sqft=round(sum_sqft, 2))

    except Exception as ex:
        print("EXCEPTION OCCURED:")
        print(ex)
        return render_template("error_404.html")


def delete_view(projectName, rowNumber):
    md = database.MongoDatabase()
    query = {'projectName': projectName}
    try:
        md.updateData(query, '$pull', {'dims': {'dimId': int(rowNumber)}})
        return redirect(url_for('record', projectName=projectName))
    except Exception as e:
        print("EXCEPTION OCCURED:")
        print(e)
        return render_template("error_404.html")


def deleteProject_view(projectName):
    md = database.MongoDatabase()

    if md.deleteData(projectName):
        return redirect(url_for('index'))
