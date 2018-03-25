import os
import prepare
import string
import random

from django.test import SimpleTestCase
from django.test import TestCase
from django.core import exceptions
from django.db import transaction
from django.db import utils
from django.core import exceptions
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


class PackageModelTest(TestCase):
    """
    Test package model and methods
    """

    def test_can_build_model(self):
        desc = 'short description'
        package = Package(description=desc)
        self.assertIsNotNone(package, 'could not build package')
        self.assertEqual(package.description, desc, 'package built wrong')
        self.assertEqual(str(package), desc, 'package not human readable')

    def test_description_size_limit(self):
        max_len = 140
        long_desc = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(max_len + 1))
        package = Package(description=long_desc)
        try:
            package.save()
            self.fail('Descriptors longer than '+max_len+' chars allowed')
        except utils.DataError:
            pass

    def test_can_persist_model(self):
        package = Package(description='short description')
        package.save()
        test_pkg = Package(package.pk)
        test_pkg.refresh_from_db()
        self.assertEqual(package.description, test_pkg.description)
        new_desc = 'new description'
        package.description = new_desc
        package.save()
        test_pkg.refresh_from_db()
        self.assertEqual(test_pkg.description, new_desc)

    def test_can_delete_model(self):
        package = Package(description='unnec')
        package.save()
        test_pkg = Package(package.pk)
        test_pkg.refresh_from_db()
        self.assertEqual(package.description, test_pkg.description)
        package.delete()
        try:
            test_pkg.refresh_from_db()
            self.fail('Package was not deleted')
        except exceptions.ObjectDoesNotExist:
            pass


class StatusModelTest(TestCase):
    """
    Test package status model and methods
    """

    def test_can_build_and_save_model(self):
        pkg = Package(description='unnec')
        pkg.save()
        data = {'latitude': 90, 'longitude': 180, 'elevation': 1}
        status = Status(package=pkg, **data)
        self.assertIsNotNone(status)
        status.save()
        self.assertIsNotNone(status.pk)

    def test_cannot_save_invalid_data(self):
        """
        TODO PROPER MODEL VALIDATION
        latitude range is -90 -> 90
        longitude range is -180 -> 180
        elevation range is -99999 -> 99999
        """
        pkg = Package(description='unnec')
        pkg.save()
        data = {'latitude': -100, 'longitude': 240, 'elevation': 1000000}
        status = Status(package=pkg, **data)
        fail_msg = 'invalid data{0} allowed'
        try:
            with transaction.atomic():
                status.save()
            self.fail(fail_msg.format(data))
        except:
            pass
        data['latitude'] = 45  # set only latitude to valid
        try:
            with transaction.atomic():
                status.save()
            self.fail(fail_msg.format(data))
        except:
            pass
        data['longitude'] = 0  # set only longitude to valid
        try:
            with transaction.atomic():
                status.save()
            self.fail(fail_msg.format(data))
        except:
            pass
