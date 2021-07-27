from flask import Flask, render_template, redirect, session, request
import random
import string

import database
import app
import helper

app = user_auth = Flask(__name__)


def index_view():
    print("INDEX-VIEW:", session)
    return render_template('index.html')


def records_view():
    # try:
    #     name = request.form['name']
    #     length = request.form['length']
    #     width = request.form['width']
    #     rate = request.form['rate']
    return render_template('records.html')
