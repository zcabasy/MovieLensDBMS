FROM python:latest
COPY . /microservices/use-case-2
WORKDIR /microservices/use-case-2
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["use-case-2.py"]