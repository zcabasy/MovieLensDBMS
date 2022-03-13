FROM python:latest
COPY . /microservices/data-catalogue
WORKDIR /microservices/data-catalogue
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]s
CMD ["data-catalogue.py"]