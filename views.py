from flask import Flask, render_template, redirect, session, request
import random
import string

import database
import app

app = user_auth = Flask(__name__)


def index_view():
    print("INDEX-VIEW:", session)

    try:
        if request.method == "POST":
            name = str(request.form['new_project_name']).replace(" ", "-")
            print(name)

    except Exception as ex:
        print("EXCEPTION OCCURED: \n")
        print(ex)
    return render_template('index.html')


def records_view():
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
