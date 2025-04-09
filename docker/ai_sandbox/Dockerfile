FROM python:3.9

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt

RUN python manage.py migrate

CMD ["uwsgi", "--http-socket", "0.0.0.0:80", "--file", "/code/gpt/wsgi.py"]