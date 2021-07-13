FROM python:3.6-slim

RUN mkdir doctor-app
WORKDIR /doctor-app
ADD . /doctor-app

RUN apt-get update -y
# RUN apt-get install postgresql-10 -y
RUN apt-get install postgresql postgresql-contrib libpq-dev -y
# sRUN apt install pgadmin3 -y
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
