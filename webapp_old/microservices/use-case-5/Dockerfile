FROM python:latest
COPY . /microservices/use-case-5
WORKDIR /microservices/use-case-5
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-5.py"]