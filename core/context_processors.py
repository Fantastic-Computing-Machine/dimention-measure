import os

from django.conf import settings


def global_settings(request):
    return {
        "expense_enabled": settings.EXPENSE_ENABLED,
        "estimator_enabled": settings.ESTIMATE_ENABLED,
    }
