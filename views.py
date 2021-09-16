from datetime import datetime
from logging import FileHandler
import os
from openpyxl import Workbook
from flask import Flask, render_template, redirect, session, request, flash, url_for
from flask import send_file, after_this_request
from pymongo.message import query

import database
import app


app = Flask(__name__)


def index_view():
    if request.method == "POST":
        projectName = str(request.form['new_project_name']).replace(" ", "-")
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

        sum_sqm = 0.0
        sum_sqft = 0.0
        sum_amt = 0.0
        for _ in project_dimentions:
            if not isinstance(_["sqm"], str) or not isinstance(_["sqft"], str):
                sum_sqm = sum_sqm + _["sqm"]
                sum_sqft = sum_sqft + _["sqft"]

            sum_amt = sum_amt + _["amount"]

        if request.method == "POST":
            name = str(request.form['name']).replace(" ", "-")
            length = float(request.form['length'])
            width = request.form['width']
            if width == "":
                width = 0
            width = float(width)
            sqm = request.form['sqm']
            sqft = request.form['sqft']

            # print(sqm, sqft)
            if sqm.replace('.', '', 1).isdigit():
                sqm = round(float(sqm), 2)

            if sqft.replace('.', '', 1).isdigit():
                sqft = round(float(sqft), 2)

            if request.form['rate'] == '':
                rate = float(0)
                amount = float(0)
            else:
                rate = float(request.form['rate'])
                amount = float(request.form['amount'])

            max = 0
            for i in project_dimentions:
                if(i['dimId'] >= max):
                    max = i['dimId']

            new_dimentions = mdb.dimsCreator(
                max+1, name, length, width, sqm, sqft, rate, round(float(amount), 2))

            project_dimentions.append(new_dimentions)

            query = {"projectName": projectName}
            update = md.updateData(query, "$set", {"dims": project_dimentions})
            # print("Update-Status", update)

            new_dimentions = None
            return redirect(url_for('success', projectName=projectName))
        else:
            sum_sqm = round(sum_sqm, 2)
            sum_sqft = round(sum_sqft, 2)
            sum_amt = round(sum_amt, 2)

            session["proj_info"] = [projectName,
                                    project_dimentions, sum_sqm, sum_sqft, sum_amt]

            return render_template('records.html', project_json=project_dimentions, projectName=projectName, sum_sqm=sum_sqm, sum_sqft=sum_sqft, sum_amt=sum_amt)

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


def download_excel_view(projectName):
    date_time_obj = datetime.now()
    current_date = date_time_obj.strftime('%x')
    current_time = date_time_obj.strftime('%X')

    filename = "downloads/excel/" + projectName + '_' + str(current_date).replace('/', "-") + \
        '_' + str(current_time).replace(":", "-") + ".xlsx"

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = projectName

    sheet.append(["Project Name", projectName])
    sheet.append([""])
    sheet.append(["Tag", "Length", "Width", "Area | sqm",
                  "Area | sqft", "Rate", "Amount"])

    for item in session['proj_info'][1]:

        item["length"] = str(item["length"]) + " m (" + \
            str(round(item["length"]*3.281, 2)) + " ft.)"
        item["width"] = str(item["width"]) + " m (" + \
            str(round(item["width"]*3.281, 2)) + " ft.)"

        sheet.append([item["name"], item["length"],
                      item["width"], item["sqm"], item["sqft"], item["rate"], item["amount"]])

    sheet.append([""])
    sheet.append(['Total sqm', session['proj_info'][2]])
    sheet.append(['Total sqft', session['proj_info'][3]])
    sheet.append(['Total amount*', session['proj_info'][4]])

    sheet.append([""])
    sheet.append(['*Calculated using metrics in sqft.'])

    print(filename)
    workbook.save(filename=str(filename))

    session.pop('proj_info')

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
            FileHandler.close()
        except Exception as error:
            app.logger.error(
                "Error removing or closing downloaded file handle", error)
        return response

    return send_file(filename, as_attachment=True)


def download_pdf_view():
    return
