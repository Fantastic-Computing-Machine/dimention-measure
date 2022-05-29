from tabnanny import verbose
from django.apps import AppConfig


class ClientAndCompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_and_company'
    verbose_name = 'Client & Company'
