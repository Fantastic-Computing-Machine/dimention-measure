from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import *


urlpatterns = [
    path("", HomeView.as_view(), name="all_expenses"),
    # payee_id, payee_name
    path("payee/<int:pk>/<str:payee>/",
         PayeeExpensesView.as_view(), name="payee_expense")
]
