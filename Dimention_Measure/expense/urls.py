from django.urls import path

from .views import AllExpenseView, PayeeExpensesView
from .views import UpdatePayeeView
from .views import ProjectExpenseView
from .views import ProjectExpenseViews


urlpatterns = [
    path("", AllExpenseView.as_view(), name="all_expenses"),

    # payee_id, payee_name
    path("payee/<int:pk>/<str:payee>/",
         PayeeExpensesView.as_view(), name="payee_expense"),

    # payee_id, payee_name
    path("payee/<int:pk>/<str:payee>/update/",
         UpdatePayeeView.as_view(), name="payee_update"),

    #     # project_id, project_name
    #     path("project/<int:project_id>/<str:project_name>/",
    #          ProjectExpenseViews, name="project_expense"),

    # project_id, project_name
    path("project/<int:project_id>/<str:project_name>/",
         ProjectExpenseView.as_view(), name="project_expense"),


]
