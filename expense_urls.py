from flask import Blueprint, redirect, url_for

from expense_views import expense_home_view, payee_update_view, payee_delete_view
from expense_views import expense_update_view, expense_delete_view, payee_expense_view,expense_home_project_view

expense_urls = Blueprint(__name__, "expense")


@expense_urls.route("/", methods=["POST", "GET"])
def expense_home():
    return expense_home_view()

@expense_urls.route("/project/<int:pid>", methods=["POST", "GET"])
def expense_home_project(pid):
    return expense_home_project_view(pid)

@expense_urls.route('/expense/success/')
def expense_success():
    return redirect(url_for('expense_urls.expense_home'))


@expense_urls.route('/payee/delete/<int:payee_id>')
def payee_delete(payee_id):
    print("DELETE payee_id: ", payee_id)
    return payee_delete_view(payee_id)


@expense_urls.route('/payee/update/<int:payee_id>')
def payee_update(payee_id):
    return payee_update_view(payee_id)


@expense_urls.route('/exp/delete/<int:expId>')
def expense_delete(expId):
    print("DELETE expense_id: ", expId)
    return expense_delete_view(expId)


@expense_urls.route('/exp/update/<int:expId>')
def expense_update(expId):
    return expense_update_view(expId)


@expense_urls.route('/payee_expense/<string:payee>')
def payee_expense(payee):
    return payee_expense_view(payee)
