from flask import request, render_template, redirect, url_for
from datetime import datetime

from database import SqlDatabase


def expense_home_view():
    sql_obj = SqlDatabase()

    payee_list_query = "SELECT * FROM payees;"
    payee_list = sql_obj.fetchRead(payee_list_query)
    print("PAYEE LIST: ", payee_list)
    expense_list_query = "SELECT * FROM expenses;"

    expense_list = sql_obj.fetchRead(expense_list_query)
    print("EXPENSE LIST: ", expense_list)

    sum_query = "SELECT SUM(p1.amount) as sum_paid, SUM(p2.amount) as sum_gained FROM expenses p1, expenses p2 WHERE p1.payment_status='Paid' AND p2.payment_status='Recieved';"
    sum_result = sql_obj.fetchRead(sum_query)

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
            about = request.form.get('about')
            print("USER MODAL: ", new_payee, about)

            insert_expense_query = "insert into payees(payeeName, about) values('%s', '%s');" % (
                str(new_payee), str(about))
            insert_value = sql_obj.executeWrite(insert_expense_query)
            # Flashing message (successful and unsuccessful)

            return redirect(url_for('expense_urls.expense_success'))

    return render_template('expense_home.html', payee_list=payee_list, expense_list=expense_list, sum_result=sum_result)


def payee_update_view(payee_id):
    return redirect(url_for('expense_urls.expense_home'))


def payee_delete_view(payee_id):
    sql_obj = SqlDatabase()
    delete_payee_query = "DELETE FROM 'payees' WHERE payeeId='%i'" % (
        int(payee_id))
    delete_payee = sql_obj.executeWrite(delete_payee_query)
    return redirect(url_for('expense_urls.expense_home'))
