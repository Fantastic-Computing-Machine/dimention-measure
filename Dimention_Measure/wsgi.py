"""
WSGI config for Dimention_Measure project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# from whitenoise import WhiteNoise
# from whitenoise.django import DjangoWhiteNoise

try :

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dimention_Measure.settings')


    application = get_wsgi_application()


    # application = DjangoWhiteNoise(application)

    app = application

except Exception as e :
    print("Error in wsgi.py : ",e)

# from my_project import MyWSGIApp

# application = MyWSGIApp()
# application = WhiteNoise(application, root="/static")
# application.add_files("/path/to/more/static/files", prefix="more-files/")