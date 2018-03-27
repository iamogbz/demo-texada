# Trackex API

Built for [Texada Software](https://texadasoftware.com/)

[![Build Status](https://travis-ci.org/iamogbz/demo-texada.svg?branch=master)](https://travis-ci.org/iamogbz/demo-texada)

## On Your Marks

- Make sure you have **Python 3.6+** installed. If you need [installation help.](http://docs.python-guide.org/en/latest/starting/installation/)
- Create `.env` file using `.env.example`. All values are important.
- Import quick start data into database (developed and tested with **MySQL 5.7** but should play well with others)
  - `mysql [DATABASE NAME] < [PROJECT DIR]/initial_data_quickstart.sql -u [USER] -p`
- Make sure python has all requirements installed
  - `pip install -r requirements.txt`
- Add api module models to database
  - `python manage.py makemigrations api`
  - `python manage.py migrate api`

## Ready Set Go

- `python manage.py runserver [PORT]`
- Visit [http://[yourhost]:[PORT]](http://localhost:8000) to check out the browsable api
- Add .json to urls or set your header to accept json responses
  - Or simply use a web api client [![Postman](https://www.getpostman.com/favicon.ico)](https://www.getpostman.com/)
- **END POINTS**
  - `/packages` - list of packages
    - `GET` - get paginated list
    - `POST` - create new package
  - `/packages/{id}` - single pacakge
    - `GET` - get package resource
    - `PUT` `PATCH` - update package
    - `DELETE` - delete package and tracking information `PERMISSION:SUPERUSER`
  - `/packages/{id}/tracking` - package tracking
    - `GET` - paginated status list ordered by recency
    - `POST` - create new package status update
  - `/status/{id}` - status detail
    - `DELETE` - delete tracking status `PERMISSION:SUPERUSER`

## Wait Hold Up

- One way to run tests
  - `python -m unittest`
- For coverage analysis
  - `coverage run —source=. -m unittest`
  - `coverage report -m`

[![Build Status](https://travis-ci.org/iamogbz/demo-texada.svg?branch=master)](https://travis-ci.org/iamogbz/demo-texada)
