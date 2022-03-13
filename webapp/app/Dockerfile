FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:D:/Win10Documents/UCL_CS_Stuff/Year 3/COMP0022 Database and Information Management Systems/Coursework/MovieLensDBMS"
ENTRYPOINT ["python"]
CMD ["app.py"]
