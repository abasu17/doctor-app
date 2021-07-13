# doctor-app

This project is developed on Python Platform.
- **Python Version** : 3.6+
- **Flask Version** : 1.0.2

## Setup Database Environment
###### Install postgresql-10
> $ **sudo apt-get install postgresql-10**

###### Install postgresql-development environment
> $ **sudo apt-get install postgresql postgresql-contrib libpq-dev**

###### Install pgadmin3
> $ **sudo apt install pgadmin3**

## Setup Python Environment
###### Install SQLAlchemy for ORM
> $ **pip3 install psycopg2 Flask-SQLAlchemy Flask-Migrate SQLAlchemy**

## Setup Project
###### Clone GIT
> - $ **git clone https://github.com/abasu17/doctor-app**
> - $ **cd doctor-app**
> - $ **python3**

###### Setup Database
> - *>>* **from app import db**
> - *>>* **db.create_all()**
> - *>>* **exit()**

###### Run Project
> $ **python3 app.py**
