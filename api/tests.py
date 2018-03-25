import os
import prepare

from django.test import SimpleTestCase
from django.test import TestCase
from django.db.models import Model
from .models import *


class EnviromentTest(SimpleTestCase):
    """
    Test that .env file was loaded successfully
    """

    def test_has_secret_key(self):
        value = os.getenv('SECRET')
        self.assertIsNotNone(value)
        self.assertGreater(len(value), 16)

    def test_has_database_test(self):
        value = os.getenv('DB_TEST')
        self.assertIsNotNone(value)
        self.assertIsNot(value, '')

    def test_has_database_name(self):
        value = os.getenv('DB_NAME')
        self.assertIsNotNone(value)
        self.assertIsNot(value, '')

    def test_has_database_name(self):
        value = os.getenv('DB_PASS')
        self.assertIsNotNone(value)
        self.assertIsNot(value, '')

    def test_has_database_user(self):
        value = os.getenv('DB_USER')
        self.assertIsNotNone(value)
        self.assertIsNot(value, '')
