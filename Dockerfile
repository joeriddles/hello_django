FROM python:3.9 as prod
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
COPY . /app
WORKDIR /app
CMD [ "gunicorn", "--bind=0.0.0.0:8000", "hello_django.wsgi" ]

FROM prod as dev
COPY requirements.dev.txt /tmp/requirements.dev.txt
RUN pip install -r /tmp/requirements.dev.txt && rm /tmp/requirements.dev.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
