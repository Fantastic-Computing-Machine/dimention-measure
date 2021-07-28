from flask import Flask, render_template, session,request,flash
from werkzeug.utils import redirect

from views import index_view, records_view
import helper

app = Flask(__name__)
app.secret_key = "fantasticcomputingmachine"


@app.route('/' ,methods=["POST", "GET"])
def index():
    
    # Homepage
    helper.initialization()
    return index_view()



@app.route('/record/<projectName>/' ,methods=["POST", "GET"])
def record(projectName):
    helper.initialization()
    return records_view(projectName)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
