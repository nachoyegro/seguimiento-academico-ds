FROM python:3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app

#Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]
