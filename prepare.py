import os

import django
from dotenv import load_dotenv

from trackex import wsgi

load_dotenv(verbose=True, dotenv_path='.env')
django.setup()
