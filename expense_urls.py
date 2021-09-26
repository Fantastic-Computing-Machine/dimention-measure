from flask import Blueprint, redirect, url_for

from expense_views import expense_home_view, payee_update_view, payee_delete_view

expense_urls = Blueprint(__name__, "expense")


@expense_urls.route("/", methods=["POST", "GET"])
def expense_home():
    return expense_home_view()


@expense_urls.route('/expense/success/')
def expense_success():
    return redirect(url_for('expense_urls.expense_home'))


@expense_urls.route('/expense/payee/delete/<payee_id>')
def payee_delete(payee_id):
    return payee_delete_view(payee_id)


@expense_urls.route('/expense/payee/update/<payee_id>')
def payee_update(payee_id):
    return payee_update_view(payee_id)
