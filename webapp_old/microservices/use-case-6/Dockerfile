FROM python:latest
COPY . /microservices/use-case-6
WORKDIR /microservices/use-case-6
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-6.py"]