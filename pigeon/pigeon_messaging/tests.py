from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.compat import coreapi, requests
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 RequestsClient)
from account.models import Account
from pigeon_messaging.models import Message


class CreateMessageTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/api/messages/messages-list'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
        # Create 2 Account objects to have an example conversation
        # First User
        account = Account.objects.create(
            username="userone", email="userone@gmail.com")
        account.set_password('password123')
        account.save()
        # Second User
        account = Account.objects.create(
            username="usertwo", email="usertwo@gmail.com")
        account.set_password('password123')
        account.save()

    def test_message_create_successful(self):
        self.data = {
            "content": "Sample Text Message",
            "read": 'false',
            "sender": "1",  # Account ID of userone
            "receiver": "2",  # Account ID of userone
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)

    def test_message_create_unauthorized(self):
        self.data = {
            "content": "Sample Text Message",
            "read": 'false',
            "sender": "1",  # Account ID of userone
            "receiver": "2",  # Account ID of userone
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_message_create_nosender(self):
        self.data = {
            "content": "Sample Text Message",
            "read": 'false',
            "receiver": "2",
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), 0)


class UpdateMessageTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/api/messages/messages-list'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
        # Create 2 Account objects to have an example conversation
        # First User
        account = Account.objects.create(
            username="userone", email="userone@gmail.com")
        account.set_password('password123')
        account.save()
        # Second User
        account = Account.objects.create(
            username="usertwo", email="usertwo@gmail.com")
        account.set_password('password123')
        account.save()

        self.data = {
            "content": "Sample Text Message",
            "read": 'false',
            "sender": "1",  # Account ID of userone
            "receiver": "2",  # Account ID of userone
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)

    def test_message_update_successful(self):
        # Change the data
        self.data = {
            "content": "Sample Text Message Edited",
            "read": 'false',
        }
        self.url = "http://127.0.0.1:8000/api/messages/message/1/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,  status.HTTP_200_OK)

    # Try to update a Message object that doesn't exist
    def test_message_update_msgnotfound(self):
        # Change the data
        self.data = {
            "content": "Sample Text Message Edited",
            "read": 'false',
        }
        self.url = "http://127.0.0.1:8000/api/messages/message/3/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,  status.HTTP_404_NOT_FOUND)

    def test_message_update_unauthorized(self):
        self.client.logout()
        self.data = {
            "content": "Sample Text Message Edited",
            "read": 'false',
        }
        self.url = "http://127.0.0.1:8000/api/messages/message/1/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class DeleteMessageTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/api/messages/messages-list'
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
    # Create 2 Account objects to have an example conversation
        # First User
        account = Account.objects.create(
            username="userone", email="userone@gmail.com")
        account.set_password('password123')
        account.save()
        # Second User
        account = Account.objects.create(
            username="usertwo", email="usertwo@gmail.com")
        account.set_password('password123')
        account.save()

        self.data = {
            "content": "Sample Text Message",
            "read": 'false',
            "sender": "1",  # Account ID of userone
            "receiver": "2",  # Account ID of userone
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)

    def test_message_delete_successful(self):
        self.url = "http://127.0.0.1:8000/api/messages/message/1/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(Message.objects.count(), 0)

    def test_message_delete_unauthorized(self):
        self.client.logout()
        self.url = "http://127.0.0.1:8000/api/messages/message/1/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    # No such Message object

    def test_message_delete_unsuccessful(self):
        self.url = "http://127.0.0.1:8000/api/messages/message/3/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
