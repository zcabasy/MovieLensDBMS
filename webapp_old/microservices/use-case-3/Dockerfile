FROM python:latest
COPY . /microservices/use-case-3
WORKDIR /microservices/use-case-3
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-3.py"]