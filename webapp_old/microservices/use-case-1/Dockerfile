FROM python:latest
COPY . /microservices/use-case-1
WORKDIR /microservices/use-case-1
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-1.py"]