from flask import Flask, render_template, redirect, session, request
import random
import string

# import database
import app

app = user_auth = Flask(__name__)


def index_view():
    return render_template('index.html')

def records_view():
    return render_template('records.html')