from flask import request, render_template, redirect


def expense_home_view():
    if request.method == 'POST':
        if request.form['expenseModal']:
            print("hello")
            return redirect('index')
        elif request.form['userModal']:
            print("hello2")
            return render_template("error_404.html")

    return render_template('expense_home.html')
