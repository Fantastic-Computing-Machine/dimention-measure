# Fantastic Computing Machine

Deploying ML models

# Getting Started

## On Ubuntu Platform

1.  Create a Virtual Environment. Here **env** is the environment name

        python3 -m venv env

2.  Activate the Environmnt to Install the dependencies:

        source env/bin/activate

3.  Install the dependencies from **requirements.txt** file:

        pip install -r requirements.txt

4.  Now the **Flask App** is ready to run using:

        flask run
           OR
        python app.py
           OR
        FLASK_APP=app.py FLASK_ENV=development flask run

#