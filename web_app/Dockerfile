FROM python:3.9

WORKDIR /web-app

COPY Requirements.txt .

RUN pip install -r Requirements.txt

COPY ./app ./app

CMD ["python", "app/web_app_main.py"]