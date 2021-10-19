from flask import Blueprint, redirect, url_for

# from expense_views import expense_home_view, payee_update_view, payee_delete_view
# from expense_views import expense_update_view, expense_delete_view, payee_expense_view, project_expense_view
# from expense_views import expense_project_delete_view, payee_project_delete_view

from expense_views import *


expense_urls = Blueprint(__name__, "expense")


@expense_urls.route("/", methods=["POST", "GET"])
# Universal Expenses
def expense_home():
    return expense_home_view()


@expense_urls.route("<string:projectName>/record/<int:pid>/", methods=["POST", "GET"])
# Project specific Expense
def project_expense(projectName, pid):
    return project_expense_view(projectName, pid)


@expense_urls.route('/expense/success/')
# Universal success url for redirect
def expense_success():
    return redirect(url_for('expense_urls.expense_home'))


@expense_urls.route('/expense/<string:projectName>/<int:pid>/success/')
# Project Specific success url for redirect
def expense_project_success(projectName, pid):
    return redirect(url_for('expense_urls.project_expense', projectName=projectName, pid=pid))


@expense_urls.route('/payee/delete/<int:payee_id>/')
# Universal delete payee
def payee_delete(payee_id):
    print("DELETE payee_id: ", payee_id)
    return payee_delete_view(payee_id)


@expense_urls.route('/payee/<string:projectName>/delete/<int:pid>/<int:payee_id>/')
# Project Specific delete payee
def payee_project_delete(payee_id, projectName, pid):
    print("DELETE payee_id: ", payee_id)
    return payee_project_delete_view(payee_id, projectName, pid)


@expense_urls.route('/payee/update/<int:payee_id>/')
# Universal update payee
def payee_update(payee_id):
    return payee_update_view(payee_id)
    
@expense_urls.route('/payee/<string:projectName>/update/<int:pid>/<int:payee_id>/')
# Project Specific update payee
def payee_project_update(payee_id, projectName, pid):
    print("UPDATE payee_id: ", payee_id)
    return payee_project_update_view(payee_id, projectName, pid)


@expense_urls.route('/expense/delete/<int:expId>/')
# Universal delete expense
def expense_delete(expId):
    print("DELETE expense_id: ", expId)
    return expense_delete_view(expId)


@expense_urls.route('/expense/<string:projectName>/delete/<int:expId>/<int:pid>/')
# Project Specific delete expense
def expense_project_delete(expId, pid, projectName):
    print("DELETE expense_id: ", expId)
    return expense_project_delete_view(expId, pid, projectName)


@expense_urls.route('/exp/update/<int:expId>/')
# Universal update expense
def expense_update(expId):
    return expense_update_view(expId)


@expense_urls.route('/payee_expense/<string:payee>/')
def payee_expense(payee):
    return payee_expense_view(payee)
