# option_settings:
#   aws: elasticbeanstalk: container: python:
#     WSGIPath: myproject.wsgi: application

# container_commands:
#   01_collectstatic:
#     command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"

#   02_migrate:
#     command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"

#   03_createsuperuser:
#     command: "source /var/app/venv/*/bin/activate && python manage.py createsuperuser --noinput"

#   04_startapp:
#     command: "source /var/app/venv/*/bin/activate && python manage.py startapp myapp"

#   05_createinitialrevisions:
#     command: "source /var/app/venv/*/bin/activate && python manage.py createinitialrevisions --noinput"

#   06_applymigrations:
#     command: "source /var/app/venv/*/bin/activate && python manage.py applymigrations --noinput"

#   07_syncsearchindex:
#     command: "source /var/app/venv/*/bin/activate && python manage.py syncsearchindex --noinput"

#   08_createsampledata:
#     command: "source /var/app/venv/*/bin/activate && python manage.py createsampledata --noinput"

#   09_createsampleusers:
#     command: "source /var/app/venv/*/bin/activate && python manage.py createsampleusers --noinput"

#   10_rebuildsearchindex:
#     command: "source /var/app/venv/*/bin/activate && python manage.py rebuildsearchindex --noinput"

#   11_recreateindex:
#     command: "source /var/app/venv/*/bin/activate && python manage.py recreateindex --noinput"

#   12_runserver:
#     command: "source /var/app/venv/*/bin/activate && python manage.py runserver 0.0.0.0:80"

# option_settings:
#   aws: elasticbeanstalk: application: environment:
#     DJANGO_SETTINGS_MODULE: "myproject.settings"

# files:
#   "/opt/elasticbeanstalk/hooks/appdeploy/post/99_make_logs_writable.sh":
#     mode: "000755"
#     owner: root
#     group: root
#     content: |
#     #!/bin/bash
#     chmod o+w / var/log/nginx/error.log
#     chmod o+w / var/log/nginx/access.log
#     chmod o+w / var/log/nginx/healthd/application.log
