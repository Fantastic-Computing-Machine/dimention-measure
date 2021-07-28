from flask import Flask, render_template, session

from views import index_view, records_view
import helper

app = Flask(__name__)
app.secret_key = "fantasticcomputingmachine"


@app.route('/')
def index():
    # Homepage
    helper.initialization()
    return index_view()


@app.route('/record/', methods=["POST", "GET"])
def record():
    helper.initialization()
    return records_view()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
