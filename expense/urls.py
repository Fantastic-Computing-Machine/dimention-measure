from django.urls import path

from .views import (
    AllExpenseView,
    PayeeExpensesView,
    UpdatePayeeView,
    ProjectExpenseView,
    UpdateExpenseView,
    DeleteExpenseView,
    DeletePayeeView,
)

urlpatterns = [
    path("", AllExpenseView.as_view(), name="all_expenses"),

    # payee_id, payee_name
    path("payee/<int:pk>/<str:payee>/",
         PayeeExpensesView.as_view(), name="payee_expense"),

    # payee_id, payee_name
    path("payee/<int:pk>/<str:payee>/update/",
         UpdatePayeeView.as_view(), name="payee_update"),

    # expense_id, project_name
    path("expense/<int:pk>/<int:project_id>/<str:project_name>/update/",
         UpdateExpenseView.as_view(), name="expense_update"),

    # project_id, project_name
    path("project/<int:project_id>/<str:project_name>/",
         ProjectExpenseView.as_view(), name="project_expense"),

    # payee_id, project_id, project_name
    path("payee/<int:payee_id>/<int:project_id>/<str:project_name>/delete/",
         DeletePayeeView, name="delete_Payee_Project"),

    # payee_id, project_id, project_name
    path("expense/<int:expense_id>/<int:project_id>/<str:project_name>/delete/",
         DeleteExpenseView, name="delete_expense"),
]
