import os

import django
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trackex.settings")

load_dotenv(verbose=True, dotenv_path='.env')
django.setup()
