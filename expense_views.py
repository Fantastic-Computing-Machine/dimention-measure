from flask import request, render_template, redirect, url_for
from datetime import datetime

from database import SqlDatabase


def expense_home_view():
    sql_obj = SqlDatabase()

    payee_list_query = "SELECT payeeName FROM payees;"
    payee_list = sql_obj.fetchRead(payee_list_query)
    print("PAYEE LIST: ", payee_list)
    expense_list_query = "SELECT * FROM expenses;"
    # payee, amount, date_created, payment_status
    expense_list = sql_obj.fetchRead(expense_list_query)
    print("EXPENSE LIST: ", expense_list)

    if request.method == 'POST':
        print(request.form)
        if "expenseModal" in request.form:
            amount = request.form.get('amount')
            payee = request.form.get('payee_list')
            status = request.form.get('status_radio')
            print("EXPENSE MODAL: ", amount, payee, status)

            insert_expense_query = "insert into expenses(payee, amount, payment_status) values('%s', '%f', '%s');" % (
                str(payee), float(amount), str(status))
            insert_value = sql_obj.executeWrite(insert_expense_query)
            # Flashing message (successful and unsuccessful)

            return redirect(url_for('expense_urls.expense_success'))

        elif "userModal" in request.form:
            new_payee = request.form.get(
                'newPayeeName').strip().replace(' ', "-")
            print("USER MODAL: ", new_payee)

            insert_expense_query = "insert into payees(payeeName) values('%s');" % (
                str(new_payee))
            insert_value = sql_obj.executeWrite(insert_expense_query)
            # Flashing message (successful and unsuccessful)

            return redirect(url_for('expense_urls.expense_success'))

    return render_template('expense_home.html', payee_list=payee_list, expense_list=expense_list)
