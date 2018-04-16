# Trackex API

Built for [Texada Software](https://texadasoftware.com/)

[![Build Status](https://travis-ci.org/iamogbz/demo-texada.svg?branch=master)](https://travis-ci.org/iamogbz/demo-texada)
[![Coverage Status](https://coveralls.io/repos/github/iamogbz/demo-texada/badge.svg?branch=master)](https://coveralls.io/github/iamogbz/demo-texada?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/4c2b22402ea39b2360f8/maintainability)](https://codeclimate.com/github/iamogbz/demo-texada/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce2937145fc34d54a420688976398f7e)](https://www.codacy.com/app/iamogbz/demo-texada)

## On Your Marks

- Make sure you have **Python 3.6+** installed. If you need [installation help.](http://docs.python-guide.org/en/latest/starting/installation/)
- Create `.env` file using `.env.example`. All values are important.
- Make sure python has all requirements installed
  - `pip install -r requirements.txt`
- Run database migrations
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Import quick start data
  - `python manage.py loaddata trackex/fixtures/initial_data_auth.json`
  - `python manage.py loaddata api/fixtures/initial_data_api.json`

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
  - `python manage.py test`
- For coverage analysis
  - `coverage run --source=. manage.py test`
  - `coverage report -m`

[![Build Status](https://travis-ci.org/iamogbz/demo-texada.svg?branch=master)](https://travis-ci.org/iamogbz/demo-texada)
[![Coverage Status](https://coveralls.io/repos/github/iamogbz/demo-texada/badge.svg?branch=master)](https://coveralls.io/github/iamogbz/demo-texada?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/4c2b22402ea39b2360f8/maintainability)](https://codeclimate.com/github/iamogbz/demo-texada/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce2937145fc34d54a420688976398f7e)](https://www.codacy.com/app/iamogbz/demo-texada)
