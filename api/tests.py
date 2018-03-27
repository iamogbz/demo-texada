import os
import prepare
import string
import random
import decimal

from django.test import SimpleTestCase
from django.test import TestCase
from django.core import exceptions
from django.db import transaction
from django.db import utils
from .models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class EnviromentTest(SimpleTestCase):
    """
    Test that .env file was loaded successfully
    """

    def test_has_database_config(self):
        for v in ['DB_TEST', 'DB_NAME', 'DB_PASS', 'DB_USER', 'SECRET']:
            value = os.getenv(v)
            fail_msg = 'missing "{0}" in .env'.format(v)
            self.assertIsNotNone(value, fail_msg)
            if v == 'SECRET':
                fail_msg = 'env {0} should be at least 16 characters'.format(v)
                self.assertGreater(len(value), 16, fail_msg)
            else:
                self.assertIsNot(value, '', fail_msg)


class FixtureTestCase(APITestCase):
    # fixtures to load for testing
    fixtures = ['initial_data_api.json', 'initial_data_auth.json']


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
        limit = 140
        long_desc = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(limit + 1))
        package = Package(description=long_desc)
        try:
            package.save()
            self.fail('Descriptor longer than {0} chars allowed'.format(limit))
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
        self.assertEqual(str(status),
                         "{0} at lat({1}) lng({2}), {3} metres high"
                         .format(status.created, status.latitude,
                                 status.longitude, status.elevation),
                         'Status fails string representation')
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
        valid_data = {'latitude': 45, 'longitude': 0}
        fail_msg = 'invalid data{0} allowed'

        for k in data:
            if k in valid_data:
                data[k] = valid_data[k]
            try:
                status = Status(package=pkg, **data)
                with transaction.atomic():
                    status.save()
                self.fail(fail_msg.format(data))
            except decimal.InvalidOperation:
                pass


class ApiEndpointsTest(FixtureTestCase):
    """
    Test package url endpoints
    thus also checking serializers, views
    """

    def assert_http(self, response, status, message=None):
        self.assertEqual(response.status_code, status, message)

    def assert_has_fields(self, resp, msg, *fields):
        for f in fields:
            self.assertIsNotNone(resp.data[f], msg.format(f))

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
        fields = ['id', 'url', 'status', 'tracking', 'description']
        self.assert_has_fields(response, 'Package data missing {0}', *fields)
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

    def test_get_status(self):
        """
        Test getting single status
        Test get missing status
        """
        url = reverse('status-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_404_NOT_FOUND,
                         'Wrong response for missing status')
        url = reverse('status-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assert_http(response, status.HTTP_200_OK,
                         'Wrong response for status-detail')

        fields = ['package', 'latitude', 'longitude', 'elevation', 'created']
        self.assert_has_fields(response, 'Tracking data missing {0}', *fields)

    def test_update_status(self):
        """
        Test update with PUT not allowed
        Test update with POST not allowed
        Test update with PATCH not allowed
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user)
        data = {'latitude': 90, 'longitude': 180, 'elevation': 1}
        url = reverse('status-detail', kwargs={'pk': 2})
        response = self.client.put(url, data)
        self.assert_http(response, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "Status can be modified with PUT")
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "Status can be modified with POST")
        response = self.client.patch(url, data)
        self.assert_http(response, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "Status can be modified with PATCH")

    def test_delete_status(self):
        """
        Test delete without authorisation
        Test delete status
        """
        user = User.objects.get(username='demoer')
        self.client.force_authenticate(user)
        url = reverse('status-detail', kwargs={'pk': 4})
        response = self.client.delete(url)
        self.assert_http(response, status.HTTP_403_FORBIDDEN,
                         "Status deleted without proper permission")
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user)
        response = self.client.delete(url)
        self.assert_http(response, status.HTTP_204_NO_CONTENT,
                         "Wrong http status for successful deletion")

    def test_get_package_statuses(self):
        """
        Test get package tracking list
        Test pagination
        """
        url = reverse('package-tracking', kwargs={'pk': 2})
        limit = 1
        response = self.client.get(url, {'limit': limit, 'offset': 1})
        self.assert_http(response, status.HTTP_200_OK,
                         "Can not package tracking history")
        self.assertEqual(len(response.data['results']), limit,
                         'List not properly paginated')
        limit = 10
        response = self.client.get(url, {'limit': limit, 'offset': 0})
        self.assertLessEqual(len(response.data['results']),
                             limit, 'List not properly paginated')
        self.assertNotIn('package', response.data['results'][0],
                         'Status has redundant package field')

    def test_update_package_status(self):
        """
        Test add package status
        """
        msg_tmpl = 'Wrong response to invalid data {0}'
        url = reverse('package-tracking', kwargs={'pk': 3})
        data = {'latitude': -100, 'longitude': 240, 'elevation': 1000000}
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_403_FORBIDDEN,
                         "Should have gotten a forbidden status")
        user = User.objects.get(username='demoer')
        self.client.force_authenticate(user)
        valid_data = {'longitude': 0, 'elevation': 1000}
        for k in data:
            if k in valid_data:
                data[k] = valid_data[k]
            response = self.client.post(url, data)
            self.assert_http(response, status.HTTP_400_BAD_REQUEST,
                             msg_tmpl.format(data))
        data['latitude'] = 45  # set only latitude to valid
        response = self.client.post(url, data)
        self.assert_http(response, status.HTTP_201_CREATED,
                         "Status not successfully created")
        self.assertEqual(45, response.data['latitude'],
                         'Incorrect tracking details created')
