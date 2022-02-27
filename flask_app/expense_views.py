from flask import request, render_template, redirect, url_for, flash
import time
from datetime import datetime

from database import SqlDatabase


def expense_home_view():
    # Universal Expenses
    sql_obj = SqlDatabase()

    payee_list_query = "SELECT payeeId, payeeName, remarks FROM payees;"
    payee_list = sql_obj.fetchRead(payee_list_query)
    print("PAYEE LIST: ", payee_list)
    expense_list_query = "SELECT * FROM expenses order by date_created DESC;"

    expense_list = sql_obj.fetchRead(expense_list_query)
    print("EXPENSE LIST: ", expense_list)

    sum_query = '''SELECT T1.sum_paid as sum_paid, T2.sum_recieved as sum_recieved FROM(
                (SELECT SUM(amount) as sum_paid, @rn1 := @rn1 + 1 AS row_number1 
                FROM expenses,(SELECT @rn1 := 0 ) var WHERE payment_status='Paid') as T1 inner join 
                (SELECT SUM(amount) as sum_recieved, @rn2 := @rn2 + 1 AS row_number2 
                FROM expenses ,(SELECT @rn2 := 0 ) var WHERE payment_status='Recieved' )as T2 ON T1.row_number1 = T2.row_number2); '''
    sum_result = sql_obj.fetchRead(sum_query)

    if request.method == 'POST':
        print(request.form)
        # if "expenseModal" in request.form:
        #     amount = request.form.get('amount')
        #     payee = request.form.get('payee_list')
        #     status = request.form.get('status_radio')
        #     print("EXPENSE MODAL: ", amount, payee, status)

        #     insert_expense_query = "insert into expenses(payee, amount, payment_status) values('%s', '%f', '%s');" % (
        #         str(payee), float(amount), str(status))
        #     insert_value = sql_obj.executeWrite(insert_expense_query)
        #     if insert_value == False:
        #         flash("Something Went Wrong :( Error code S04")
        #         # flash("Successfully Added :)")
        #     # else:
        #     # Flashing message (successful and unsuccessful)

        #     return redirect(url_for('expense_urls.expense_success'))

        if "userModal" in request.form:
            new_payee = request.form.get(
                'newPayeeName').strip().replace(' ', "-")
            remarks = request.form.get('remarks')
            print("USER MODAL: ", new_payee, remarks)

            insert_expense_query = "insert into payees(payeeName, remarks) values('%s', '%s');" % (
                str(new_payee), str(remarks))
            insert_value = sql_obj.executeWrite(insert_expense_query)
            if insert_value == False:
                flash("Something Went Wrong :( Error code S04")

            # return redirect(url_for('expense_urls.expense_success'))

        elif "expense_update" in request.form:
            expId = request.form.get('expId')
            amount_update = request.form.get('amount')
            payee_update = request.form.get('payee_list')
            ts = time.time()
            timestamp = datetime.fromtimestamp(
                ts).strftime('%Y-%m-%d %H:%M:%S')
            print(timestamp)

            print(expId, amount_update, payee_update)
            update_query = "UPDATE expenses SET amount=%f, payee='%s', date_created='%s' WHERE expId=%i;" % (
                float(amount_update), str(payee_update), str(timestamp), int(expId))

            print(update_query)
            update_value = sql_obj.executeWrite(update_query)
            if update_value is False:
                print("FAILED")
                flash("Something Went Wrong :( Error code S02")
                return render_template("error_404.html")
            print("TRUE")
            # return redirect(url_for('expense_urls.expense_success'))

        elif "payee_update" in request.form:
            payee_update = request.form.get('payee_list')
            print(amount_update, payee_update)

            # return redirect(url_for('expense_urls.expense_success'))

        elif "payee_update" in request.form:
            sql_obj = SqlDatabase()
            # payeeName = request.form.get('payeeName')
            # remarks = request.form.get('remarks')
            # payee_id = request.form.get('payee_id')
#           update_payee_query = "UPDATE payees SET payeeName = '%s', remarks ='%s' WHERE payeeId=%i" % (str(payeeName), str(remarks),
#           int(payee_id))
#           update_payee = sql_obj.executeWrite(update_payee_query)
#           print("******Update STATUS: ", update_payee)
#           return redirect(url_for('expense_urls.expense_success'))
        return redirect(url_for('expense_urls.expense_success'))

    if expense_list is None:
        expense_list = []
    if payee_list is None:
        payee_list = []

    context = {
        "payee_list": payee_list,
        "expense_list": expense_list,
        "sum_result": sum_result,
    }
    return render_template('expense_home.html', **context)
    # return render_template('expense_home.html', payee_list=payee_list, expense_list=expense_list, sum_result=sum_result)


def payee_update_view(payee_id):
    sql_obj = SqlDatabase()
    update_payee_query = "UPDATE payees SET payeeName = '%s', remarks ='%s' WHERE payeeId=%i" % (
        str(payeeName), str(remarks), int(payee_id))
    update_payee = sql_obj.executeWrite(update_payee_query)
    print("******Update STATUS: ", update_payee)
    return redirect(url_for('expense_urls.expense_home'))


def payee_project_update_view(expId, pid, projectName):
    # Project Specific update payee
    return redirect(url_for('expense_urls.expense_home'))


def payee_delete_view(payee_id):
    # Universal delete payee
    sql_obj = SqlDatabase()
    delete_payee_query = "DELETE FROM payees WHERE payeeId=%i" % (
        int(payee_id))
    delete_payee = sql_obj.executeWrite(delete_payee_query)
    print("******DELETE STATUS: ", delete_payee)
    return redirect(url_for('expense_urls.expense_home'))


def payee_project_delete_view(payee_id, projectName, pid):
    # Project Specific delete payee
    sql_obj = SqlDatabase()
    delete_payee_query = "DELETE FROM payees WHERE payeeId=%i" % (
        int(payee_id))
    delete_payee = sql_obj.executeWrite(delete_payee_query)
    print("******DELETE STATUS: ", delete_payee)
    context = {
        "projectName": projectName,
        "pid": pid,
    }
    return redirect(url_for('expense_urls.expense_project_success', **context))
    # return redirect(url_for('expense_urls.expense_project_success', projectName=projectName, pid=pid))


def expense_delete_view(expId):
    # Universal delete expense
    sql_obj = SqlDatabase()
    delete_payee_query = "DELETE FROM expenses WHERE expId=%i" % (
        int(expId))
    delete_payee = sql_obj.executeWrite(delete_payee_query)
    print("******DELETE STATUS: ", delete_payee)
    return redirect(url_for('expense_urls.expense_home'))


def expense_project_delete_view(expId, pid, projectName):
    # Project Specific delete expense
    sql_obj = SqlDatabase()
    delete_payee_query = "DELETE FROM expenses WHERE expId=%i" % (
        int(expId))
    delete_payee = sql_obj.executeWrite(delete_payee_query)
    print("******DELETE STATUS: ", delete_payee)
    context = {
        "projectName": projectName,
        "pid": pid
    }
    return redirect(url_for('expense_urls.expense_project_success', **context))


def expense_update_view(expId):
    # Universal update expense
    return redirect(url_for('expense_urls.expense_home'))


def payee_expense_view(payee):
    # All expense of Payee
    sql_obj = SqlDatabase()
    query = f'''SELECT expid, payee, amount, date_created, payment_status, e1.pid, pname 
                FROM expenses e1
                INNER JOIN (SELECT pname, pid FROM projects) p1 ON p1.pid=e1.pid 
                WHERE payee='{payee}' order by date_created DESC;'''
    result = sql_obj.fetchRead(query)
    print("\nQUERY: ", query)
    print("\nRESULT: ", result)

    if result is None:
        result = []

    context = {
        "result": result,
        "payee": payee
    }
    return render_template("payee_exp.html", **context)


def project_expense_view(projectName, pid):
    # Project specific Expense
    sql_obj = SqlDatabase()

    payee_list_query = "SELECT payeeId, payeeName, remarks FROM payees;"
    payee_list = sql_obj.fetchRead(payee_list_query)
    print("PAYEE LIST: ", payee_list)
    expense_list_query = f"SELECT * FROM expenses where pid ={pid} order by date_created DESC;"

    expense_list = sql_obj.fetchRead(expense_list_query)
    print("EXPENSE LIST: ", expense_list)

    sum_query = f'''SELECT T1.sum_paid as sum_paid, T2.sum_recieved as sum_recieved FROM(
                (SELECT SUM(amount) as sum_paid, @rn1 := @rn1 + 1 AS row_number1 
                FROM expenses,(SELECT @rn1 := 0 ) var WHERE payment_status='Paid' and pid ={pid}) as T1 inner join 
                (SELECT SUM(amount) as sum_recieved, @rn2 := @rn2 + 1 AS row_number2 
                FROM expenses ,(SELECT @rn2 := 0 ) var WHERE payment_status='Recieved' and pid ={pid}) as T2 ON T1.row_number1 = T2.row_number2);'''
    sum_result = sql_obj.fetchRead(sum_query)

    context = {
        "projectName": projectName,
        "pid": pid,
    }

    if request.method == 'POST':
        print(request.form)
        if "expenseModal" in request.form:
            amount = request.form.get('amount')
            payee = request.form.get('payee_list')
            status = request.form.get('status_radio')
            print("EXPENSE MODAL: ", amount, payee, status)

            insert_expense_query = f"insert into expenses(payee, amount, payment_status,pid) values('{str(payee)}', {float(amount)}, '{str(status)}',{int(pid)});"
            insert_value = sql_obj.executeWrite(insert_expense_query)
            if insert_value == False:
                flash("Something Went Wrong :( Error code S04")

            # return redirect(url_for('expense_urls.expense_project_success', **context))

        elif "userModal" in request.form:
            new_payee = request.form.get(
                'newPayeeName').strip().replace(' ', "-")
            remarks = request.form.get('remarks')
            print("USER MODAL: ", new_payee, remarks)

            insert_expense_query = f"insert into payees(payeeName, remarks) values('{str(new_payee)}', '{str(remarks)}');"
            insert_value = sql_obj.executeWrite(insert_expense_query)
            if insert_value == False:
                flash("Something Went Wrong :( Error code S04")

            # return redirect(url_for('expense_urls.expense_project_success', **context))

        elif "expense_update" in request.form:
            expId = request.form.get('expId')
            amount_update = request.form.get('amount')
            payee_update = request.form.get('payee_list')
            ts = time.time()
            timestamp = datetime.fromtimestamp(
                ts).strftime('%Y-%m-%d %H:%M:%S')
            print(timestamp)

            print(expId, amount_update, payee_update)
            update_query = "UPDATE expenses SET amount=%f, payee='%s', date_created='%s' WHERE expId=%i;" % (
                float(amount_update), str(payee_update), str(timestamp), int(expId))

            print(update_query)
            update_value = sql_obj.executeWrite(update_query)
            if update_value is False:
                print("FAILED")
                flash("Something Went Wrong :( Error code S02")
                return render_template("error_404.html")
            print("TRUE")
            # return redirect(url_for('expense_urls.expense_project_success', **context))
            # return redirect(url_for('expense_urls.expense_project_success', projectName=projectName, pid=pid))

        elif "payee_update" in request.form:
            payee_update = request.form.get('payee_list')
            print(amount_update, payee_update)
            # return redirect(url_for('expense_urls.expense_project_success', **context))

        elif "payee_update" in request.form:
            sql_obj = SqlDatabase()
        #   payeeName = request.form.get('payeeName')
        #   remarks = request.form.get('remarks')
        #   payee_id = request.form.get('payee_id')
#           update_payee_query = "UPDATE payees SET payeeName = '%s', remarks ='%s' WHERE payeeId=%i" % (str(payeeName), str(remarks),
#           int(payee_id))
#           update_payee = sql_obj.executeWrite(update_payee_query)
#           print("******Update STATUS: ", update_payee)
#           return redirect(url_for('expense_urls.payee_project_update',projectName = projectName,pid=pid,payee_id=payee_id))

            # return redirect(url_for('expense_urls.expense_project_success', **context))
        return redirect(url_for('expense_urls.expense_project_success', **context))

    if expense_list is None:
        expense_list = []
    if payee_list is None:
        payee_list = []

    context = {
        "payee_list": payee_list,
        "expense_list": expense_list,
        "sum_result": sum_result,
        "projectName": projectName,
        "pid": pid
    }
    # context["payee_list"] = payee_list
    # context["expense_list"] = expense_list
    # context["sum_result"] = sum_result
    return render_template('expense_project.html', **context)
