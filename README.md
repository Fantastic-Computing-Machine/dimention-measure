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

CREATE TABLE PAYEES(
	payeeId int not null auto_increment,
        payeeName varchar(220) not null unique,
        primary key(payeeId)
);

create table expenses(
	expId int not null auto_increment,
        payee varchar(220) not null,
        amount float,
        date_created datetime,
        payment_status varchar(10),
        primary key(expId),
        foreign key(payee) references payees(payeeName)
);
