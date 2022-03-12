# FROM python:3.6-slim
# RUN mkdir /dimention_app
# WORKDIR /dimention_app
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# COPY . /dimention_app/
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM python:3.9-alpine

# RUN mkdir /dimention_app
# WORKDIR /dimention_app

# RUN apt update 

# RUN pip install --upgrade pip
# COPY requirements.txt /dimention_app/

# RUN pip install -r requirements.txt

# COPY . /dimention_app/

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]