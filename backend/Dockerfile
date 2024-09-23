# Use the official Python image from the Docker Hub as the base image
FROM python:3.11-slim


WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py createsu

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
