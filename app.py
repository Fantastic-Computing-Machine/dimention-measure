from flask import Flask, render_template, redirect, session, request


from views import index_view, records_view
# import user_auth

app = Flask(__name__)
app.secret_key = "fantasticcomputingmachine"



@app.route('/')
def index():
    # Homepage
    return index_view()

@app.route('/record/')
def record():
    return records_view()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000,debug=True)
