from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.compat import coreapi, requests
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 RequestsClient)
from rest_framework.authtoken.models import Token
from account.models import Account


class RegisterAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "password321",
            "password_verify": "password321"
        }
        self.url = 'http://127.0.0.1:8000/api/account/'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()

    # Successful Registration

    def test_register_successful(self):
        self.current_account_counts = Account.objects.count()
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(),
                         self.current_account_counts+1)
    # Fail registration - unauthorized

    def test_register_fail_unauthorized(self):
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    # Fail registration -  username already in-use
    # Need to run the same POST request twice because after each testing method executes
    # the data in the testing database is wiped out
    def test_register_fail_username_not_unique(self):
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class UpdateAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "password321",
            "password_verify": "password321"
        }
        self.url = 'http://127.0.0.1:8000/api/account/'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()

    def test_update_account_successful(self):
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        # Perform PUT operations on an existing Account object
        target_user_account = Account.objects.get(
            username='testuser')
        self.new_data = {
            "username": "pidgeonuser",
            "email": "testuser@gmail.com",
            "password": "password321",
            "password_verify": "password321"
        }
        self.response = self.client.put(
            self.url + str(target_user_account.pk) + '/update/', self.new_data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "password321",
            "password_verify": "password321"
        }
        self.url = 'http://127.0.0.1:8000/api/account/'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()

    def test_delete_account_successful(self):
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        target_user_account = Account.objects.get(
            username='testuser')
        self.response = self.client.delete(
            self.url + str(target_user_account.pk) + '/delete/')
        # Should be 1, since we had to create a previous dummy Account object before we created another Account object for testing this method
        self.assertEqual(Account.objects.count(), 1)
