from flask import Blueprint, redirect, url_for

from expense_views import expense_home_view

expense_urls = Blueprint(__name__, "expense")


@expense_urls.route("/", methods=["POST", "GET"])
def expense_home():
    return expense_home_view()


@expense_urls.route('/expense_home/success/')
def expense_success():
    return redirect(url_for('expense_urls.expense_home'))
