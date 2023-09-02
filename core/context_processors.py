import os

def global_settings(request):
    return {'expense_enabled': os.getenv("EXPENSE_ENABLED") == 'True','estimator_enabled': os.getenv("ESTIMATE_ENABLED") == 'True'}