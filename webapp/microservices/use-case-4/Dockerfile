FROM python:latest
COPY . /microservices/use-case-4
WORKDIR /microservices/use-case-4
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-4.py"]