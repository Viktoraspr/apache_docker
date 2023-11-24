# Project Introduction

**Weather Data Collection API and Database Reporting**

This project setups a database, creates an API for metal prices collection using Live Metal Prices API, then stores,
creates last 24 hours view and creates machine learning model.

The project sets up Postgres database, creates table and view, retrieves metal prices collection from Live Metal 
Prices API, and stores the data in a Postgres database.

Data is collected, and analyses refreshed automatically using Apache Airflow mostly hourly.

Project is written in Docker environment.

## Prerequisites

- Python 3.11
- Docker

# Setup & Usage

1. Clone the repository.

```
git clone https://github.com/TuringCollegeSubmissions/vipranc-DE2.4
```
2. Navigate to the project directory:
   `cd vipranc-DE2.4`

3. Create environment and install the prerequisite Python libraries from the provided `requirements.txt` file:
```
`python -m venv`
`pip install -r requirements.txt`
```

4. Update `docker-compose.yaml` add  with database connection details and API key in `dags/config/config.py` file.
   This is then used by running docker and creating connection with DB and Live Metal Prices API.

5. Run project in docker environment:
   `docker-compose up --build`

6. Open "Airflow" webserver: http://localhost:8080/home. Login (user and password is defined in `docker-compose.
   yaml`. Default user: `airflow`, password `airflow`.

7. Run dag `Creating view 'prices_last_12'`. You need run it only once, and it creates view in DB.

8. Dag `Retrieve data and create ML model` runs every hour - retrieves prices from API, inject data to DB and 
   creates ML learning model.

## Future Improvements

- Add data validation when it's being sent to database.
- System should backup the entire database and the machine learning models every six hours and store the last twenty 
  backups.
- src folder in dags folder should be removed - it could be placed in PyPi, and it should be separate library.