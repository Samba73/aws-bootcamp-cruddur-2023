FROM python:3.10-slim-buster    

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV = development

ENV ROLLBAR_ACCESS_TOKEN='644e2ee76ca64c2eb5cbc5f1c7021483'

EXPOSE ${PORT}

ENV PYTHONUNBUFFERED=1

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]
