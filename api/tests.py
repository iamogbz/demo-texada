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
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


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


class FixtureTestCase(APITestCase):
    # fixtures to load for testing
    fixtures = ['initial_data_api.json']

    def test_fixture_loaded(self):
        # test that fixture loaded for testing
        package = Package.objects.get(id=2)
        self.assertIsNotNone(package)


class PackageModelTest(FixtureTestCase):
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
        test_pkg = Package.objects.get(id=package.pk)
        self.assertEqual(package.description, test_pkg.description)
        new_desc = 'new description'
        package.description = new_desc
        package.save()
        test_pkg.refresh_from_db()
        self.assertEqual(test_pkg.description, new_desc)

    def test_can_delete_model(self):
        package = Package.objects.get(id=2)
        statuses = Status.objects.filter(package=package).delete()
        package.delete()
        try:
            package.refresh_from_db()
            self.fail('Package was not deleted')
        except exceptions.ObjectDoesNotExist:
            pass


class StatusModelTest(FixtureTestCase):
    """
    Test package status model and methods
    """

    def test_can_build_and_save_model(self):
        pkg = Package.objects.get(id=3)
        data = {'latitude': 90, 'longitude': 180, 'elevation': 1}
        status = Status(package=pkg, **data)
        self.assertIsNotNone(status)
        status.save()
        self.assertIsNotNone(status.pk)
        created = status.created
        status.refresh_from_db()
        self.assertEqual(created, status.created)

    def test_cannot_save_invalid_data(self):
        """
        TODO PROPER MODEL VALIDATION
        latitude range is -90 -> 90
        longitude range is -180 -> 180
        elevation range is -99999 -> 99999
        """
        pkg = Package.objects.get(id=3)
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


class ApiEndpointsTest(FixtureTestCase):
    """
    Test package url endpoints
    thus also checking serializers, views
    """

    def assert_http(self, response, status, message=None):
        self.assertEqual(response.status_code, status, message)

    def test_root_endpoint(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_200_OK,
                         "Can not access api-root")

    def test_get_packages(self):
        url = reverse('package-list')
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_200_OK,
                         "Can not access package-list")
        self.assertIsNotNone(response.data['results'])

    def test_create_package(self):
        """
        Test creation of package with proper permissions
        """
        url = reverse('package-list')
        description = 'Test Package'
        data = {}
        # make unauthenticated request
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_403_FORBIDDEN,
                         "Wrong https status for unauntheticated request")
        # make request again as demoer
        user = User.objects.get(username='demoer')
        self.client.force_authenticate(user)
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_400_BAD_REQUEST,
                         "Wrong https status for bad post request")
        # make request again with valid fields
        data['description'] = description
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_201_CREATED,
                         "Package not created successfully")
        # check if all fields are non empty
        for field in ['id', 'url', 'status', 'tracking', 'description']:
            self.assertIsNotNone(response.data['id'],
                                 'Package created response missing '+field)
        self.assertEqual(response.data['description'], description,
                         'Package created has wrong information')
        # tracking data should be empty at creation
        self.assertEqual(response.data['tracking'], [],
                         'Package should not have tracking data')

    def test_get_package(self):
        url = reverse('package-detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_404_NOT_FOUND,
                         "Wrong status code for missing package")
        url = reverse('package-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_200_OK,
                         "Can not retrieve status-detail")

    def test_update_package(self):
        """
        Test modifying package with proper permissions
        """
        user = User.objects.get(username='demoer')
        self.client.force_authenticate(user)
        desc = 'NewPackageName'
        data = {'description': desc}
        url = reverse('package-detail', kwargs={'pk': 2})
        response = self.client.put(url, data)
        self.assert_http(response, status.HTTP_403_FORBIDDEN,
                         "Package modified without proper permission")
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user)
        response = self.client.put(url, data)
        self.assert_http(response, status.HTTP_200_OK,
                         "Package could not be updated")
        self.assertEqual(desc, response.data['description'],
                         "Package unsuccessfully updated")

    def test_delete_package(self):
        """
        Test deleting package with proper permissions
        """
        user = User.objects.get(username='demoer')
        self.client.force_authenticate(user)
        url = reverse('package-detail', kwargs={'pk': 2})
        response = self.client.delete(url)
        self.assert_http(response, status.HTTP_403_FORBIDDEN,
                         "Package deleted without proper permission")
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user)
        response = self.client.delete(url)
        self.assert_http(response, status.HTTP_400_BAD_REQUEST,
                         "Package with tracking info wrongly deleted")
        pkg = Package.objects.get(id=2)
        statuses = Status.objects.filter(package=pkg).delete()
        response = self.client.delete(url)
        self.assert_http(response, status.HTTP_204_NO_CONTENT,
                         "Wrong http status for successful deletion")
