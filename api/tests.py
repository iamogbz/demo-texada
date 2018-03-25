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
        self.assertIsNotNone(value, 'missing "SECRET" value in .env')
        self.assertGreater(len(value), 16,
                           '"SECRET" should be at least 16 characters')

    def test_has_database_test(self):
        value = os.getenv('DB_TEST')
        fail_msg = 'missing "DB_TEST" in .env'
        self.assertIsNotNone(value, fail_msg)
        self.assertIsNot(value, fail_msg)

    def test_has_database_name(self):
        value = os.getenv('DB_NAME')
        fail_msg = 'missing "DB_NAME" in .env'
        self.assertIsNotNone(value, fail_msg)
        self.assertIsNot(value, '', fail_msg)

    def test_has_database_pass(self):
        value = os.getenv('DB_PASS')
        fail_msg = 'missing "DB_PASS" in .env'
        self.assertIsNotNone(value, fail_msg)
        self.assertIsNot(value, '', fail_msg)

    def test_has_database_user(self):
        value = os.getenv('DB_USER')
        fail_msg = 'missing "DB_USER" in .env'
        self.assertIsNotNone(value, fail_msg)
        self.assertIsNot(value, '', fail_msg)
