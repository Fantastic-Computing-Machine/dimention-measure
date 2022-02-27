from datetime import datetime
from logging import FileHandler
import os
from openpyxl import Workbook
from flask import Flask, render_template, redirect, session, request, flash, url_for
from flask import send_file, after_this_request
from pymongo.message import query
from decimal import Decimal

import database
from sql import CrudDatabase
import app
import helper
import json
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
                query = f"insert into projects(PNAME) values('{projectName}');"
                if sql.executeWrite(query):
                    return redirect(url_for('index'))
                else:
                    print("Not working Executing write")
                    flash(
                        "Project name already exists! Please try with different name :)")
                pid = sql.fetchRead(
                    f"select PID from projects where PNAME='{str(projectName)[0]['PID']}';")

                context = {
                    "projectName": projectName,
                    "pid": pid
                }

                return redirect(url_for('record', **context))
            except Exception as e:
                print(e)

    return render_template('index.html')


def dim_checker(form_dict):
    checked_dict = dict()
    print("FORM  REQUEST: ", form_dict)

    checked_dict['tag'] = str(form_dict['tag']).strip().replace(' ', "-")
    checked_dict['length'] = float(form_dict['length'])

    if form_dict['width'] == '':
        checked_dict['width'] = 0.0
    else:
        checked_dict['width'] = float(form_dict['width'])

    checked_dict['sqm'] = float(form_dict['sqm'])
    checked_dict['sqft'] = float(form_dict['sqft'])

    if form_dict['rate'] == '':
        checked_dict['rate'] = 0.0
        checked_dict['amount'] = 0.0
    else:
        checked_dict['rate'] = float(form_dict['rate'])
        checked_dict['amount'] = float(form_dict['amount'])

    if 'dimid' in form_dict:
        checked_dict['dimid'] = form_dict['dimid']

    # print("\n\tNEW CHECKED DICT", checked_dict)
    return checked_dict


def records_view(projectName, pid):
    try:
        sql = CrudDatabase()
        project_dimentions = sql.fetchRead(
            f"SELECT * FROM dimention WHERE PID={pid};")
        if project_dimentions is None:
            project_dimentions = []

        sum_sqm, sum_sqft, sum_amt = 0.0, 0.0, 0.0

        for _ in project_dimentions:
            if not isinstance(_["sqm"], str) or not isinstance(_["sqft"], str):
                sum_sqm = sum_sqm + float(_["sqm"])
                sum_sqft = sum_sqft + float(_["sqft"])

            sum_amt = sum_amt + float(_["amount"])

        if request.method == "POST":
            print("REQUEST.FORM--> ", request.form)
            if "new_dimention" in request.form:

                checked_dict = dim_checker(request.form)

                query = "INSERT into dimention(tag, length, width, sqm, sqft, rate, amount, pid) values('%s', %f, %f, %f, %f, %f, %f, %i);" % (
                    str(checked_dict['tag']), float(checked_dict['length']), float(checked_dict['width']), float(checked_dict['sqm']), float(checked_dict['sqft']), float(checked_dict['rate']), float(checked_dict['amount']), int(pid))

                if sql.executeWrite(query):
                    new_dimentions = None
                    return redirect(url_for('success', projectName=projectName, pid=pid))
                else:
                    print("ERROR: Unsuccessful dimention append.")
                    flash("Something Went Wrong :( Error code S04")

        else:
            a = []
            for i in project_dimentions:
                checked_list = dim_checker(i)
                a.append(checked_list)

            project_dimentions = a

            session["proj_info"] = [projectName,
                                    project_dimentions, sum_sqm, sum_sqft, sum_amt]

            context = {
                "project_json": project_dimentions,
                "projectName": projectName,
                "pid": pid,
                "sum_sqm": float(sum_sqm),
                "sum_sqft": float(sum_sqft),
                "sum_amt": float(sum_amt),
            }

            return render_template('records.html', **context)

    except Exception as ex:
        print("EXCEPTION OCCURED:")
        print(ex)
        return render_template("error_404.html")


def update_dimention_view(projectName, pid, dimid):

    sql = CrudDatabase()

    dimention_values = sql.fetchRead(
        f"SELECT * FROM dimention WHERE dimid={dimid}")

    if request.method == "POST":
        # print("REQUEST.FORM--> ", request.form)

        checked_dict = dim_checker(request.form)
        # print("\nCHECKED DICT: ", checked_dict)

        update_query = "UPDATE dimention SET tag='%s', length=%f, width=%f, sqm=%f, sqft=%f, rate=%f, amount=%f WHERE dimid=%i;" % (str(checked_dict.get('tag')), float(checked_dict.get('length')), float(
            checked_dict.get('width')), float(checked_dict.get('sqm')), float(checked_dict.get('sqft')), float(checked_dict.get('rate')), float(checked_dict.get('amount')), int(dimid))
        print(update_query)
        query = sql.executeWrite(update_query)

        if query:
            return redirect(url_for('record', projectName=projectName, pid=pid))
        else:
            print("Unsuccessful")
            flash("Something Went Wrong :( Error code S02")

    context = {
        'projectName': projectName,
        'dimid': dimid,
        'item': dimention_values[0],
    }
    return render_template("update_dimention.html", **context)


def delete_view(projectName, pid, dimid):

    query = CrudDatabase().executeWrite(
        "Delete from dimention where dimid=%i;" % (int(dimid)))
    if query:
        return redirect(url_for('record', projectName=projectName, pid=pid))

    else:
        print("ERROR: Unsuccessful dimention delete.")
        flash("Something Went Wrong :( Error code S03")


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
                      item["width"], item["sqm"], item["sqft"], item["rate"], item["amount"]])

    sheet.append([""])
    sheet.append(['Total sqm', session['proj_info'][2]])
    sheet.append(['Total sqft', session['proj_info'][3]])
    sheet.append(['Total amount*', session['proj_info'][4]])

    sheet.append([""])
    sheet.append(['*Calculated using metrics in sqft.'])

    print(filename)
    workbook.save(filename=str(filename))
    workbook.close()

    session.pop('proj_info')

    @ after_this_request
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
