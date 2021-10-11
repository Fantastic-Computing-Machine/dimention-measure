from datetime import datetime
from logging import FileHandler
import os
from openpyxl import Workbook
from flask import Flask, render_template, redirect, session, request, flash, url_for
from flask import send_file, after_this_request
from pymongo.message import query

import database
from sql import CrudDatabase
import app
import helper

app = Flask(__name__)


def index_view():
    if request.method == "POST":
        projectName = str(request.form['new_project_name']).replace(" ", "-")
        if projectName in session["projectNameList"]:
            flash("Project name already exists! Please try with different name :)")
            return redirect(request.url)
        else:
            try:
                sql = CrudDatabase()
                query = "insert into projects(PNAME) values('%s');" % str(
                    projectName)
                if sql.executeWrite(query):
                    return redirect(url_for('index'))
                else:
                    print("Not working Executing write")
                    # flash
            except Exception as e:
                print(e)

    return render_template('index.html')


def records_view(projectName, pid):
    try:

        sql = CrudDatabase()
        project_dimentions = sql.fetchRead(
            "Select * from dimention where PID=%i" % (int(pid)))

        # print("###################################")
        # print(project_dimentions)
        # print("###################################")
        if project_dimentions is None:
            project_dimentions = []

        sum_sqm = 0.0
        sum_sqft = 0.0
        sum_amt = 0.0
        for _ in project_dimentions:
            if not isinstance(_["area_sqm"], str) or not isinstance(_["area_sqft"], str):
                sum_sqm = sum_sqm + _["area_sqm"]
                sum_sqft = sum_sqft + _["area_sqft"]

            sum_amt = sum_amt + _["amount"]

        if request.method == "POST":
            name = str(request.form['name']).strip().replace(' ', "-")
            length = float(request.form['length'])
            width = request.form['width']
            if width == "":
                width = 0.0
            sqm = request.form['sqm'].replace('N/A', '0')
            sqft = request.form['sqft'].replace('N/A', '0')
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

            query = "insert into dimention(tag, length, width, area_sqm, area_sqft, rate, amount, pid) values('%s', '%f', '%f', '%f', '%f', '%f', '%f', '%i');" % (
                str(name), float(length), float(width), float(sqm), float(sqft), float(rate), float(amount), int(pid))

            if sql.executeWrite(query):
                new_dimentions = None
                return redirect(url_for('success', projectName=projectName, pid=pid))
            else:
                print("ERROR: Unsuccessful dimention append.")
                # Flash

        else:
            sum_sqm = round(sum_sqm, 2)
            sum_sqft = round(sum_sqft, 2)
            sum_amt = round(sum_amt, 2)

            session["proj_info"] = [projectName,
                                    project_dimentions, sum_sqm, sum_sqft, sum_amt]

            return render_template('records.html', project_json=project_dimentions, projectName=projectName, pid=pid, sum_sqm=sum_sqm, sum_sqft=sum_sqft, sum_amt=sum_amt)

    except Exception as ex:
        print("EXCEPTION OCCURED:")
        print(ex)
        return render_template("error_404.html")


def delete_view(projectName, pid, rowNumber):

    query = CrudDatabase().executeWrite(
        "Delete from dimention where dimid=%i;" % (int(rowNumber)))
    if query:
        return redirect(url_for('record', projectName=projectName, pid=pid))

    else:
        print("ERROR: Unsuccessful dimention delete.")
        # flash


def deleteProject_view(projectName):
    query = CrudDatabase().executeWrite(
        "Delete from projects where PNAME='%s';" % (str(projectName)))
    if query:
        return redirect(url_for('index'))
        # return redirect(url_for('record', projectName=projectName, pid=pid))

    else:
        print("ERROR: Unsuccessful Project delete.")


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

        sheet.append([item["tag"], item["length"],
                      item["width"], item["area_sqm"], item["area_sqft"], item["rate"], item["amount"]])

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
