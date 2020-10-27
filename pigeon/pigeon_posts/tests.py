from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.compat import coreapi, requests
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 RequestsClient)
from account.models import Account
from pigeon_posts.models import Post


class CreatePostTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
        # Create another Account object to act as the author for a Post object
        account = Account.objects.create(
            username="originalwriter", email="originalwriter@gmail.com")
        account.set_password('password123')
        account.save()

    def test_post_create_successful(self):
        self.url = 'http://127.0.0.1:8000/api/posts/'
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog",
            "author": "1"
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_create_unauthorized(self):
        self.url = 'http://127.0.0.1:8000/api/posts/'
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog",
            "author": "1"
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class UpdatePostTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
        # Create another Account object to act as the author for a Post object
        account = Account.objects.create(
            username="originalwriter", email="originalwriter@gmail.com")
        account.set_password('password123')
        account.save()

        # Create a Post object
        self.url = 'http://127.0.0.1:8000/api/posts/'
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog",
            "author": "1"
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)

    def test_message_update_successful(self):
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog and ate the cow.",
        }
        self.url = "http://127.0.0.1:8000/api/posts/post/1/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,  status.HTTP_200_OK)

    def test_message_update_unauthorized(self):
        self.client.logout()
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog and ate the cow.",
        }
        self.url = "http://127.0.0.1:8000/api/posts/post/1/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_message_update_toolong(self):
        self.data = {
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed pharetra vel mauris nec tincidunt. Integer sed consectetur leo, nec auctor lorem. Nunc a augue fringilla, viverra erat ut, auctor lectus. In aliquet malesuada maximus. Nam leo nisl, vulputate at pulvinar vulputate, tristique a elit. Nulla luctus ultricies nibh sed rutrum. Integer viverra volutpat odio sit amet sodales. Proin id est ultrices, elementum dolor vitae, cursus purus. Curabitur at elit ut arcu dictum eleifend vitae at diam. Sed pulvinar urna diam, at hendrerit enim facilisis a. Nunc vel rhoncus nisl. Integer a nulla ac nisl volutpat pretium quis ut dui. Nullam at turpis molestie, suscipit lorem vel, laoreet nisi. Phasellus faucibus quis ligula posuere varius. Morbi at luctus lacus. Sed a imperdiet urna. Suspendisse suscipit libero id lacus tincidunt, at porttitor neque laoreet. Etiam vitae ultrices dolor. Nulla blandit eu leo non dignissim. Suspendisse non neque et nulla posuere laoreet. In metus odio, vehicula ut mollis ac, lacinia in leo. Vivamus volutpat tellus vitae ipsum imperdiet maximus."
        }
        self.url = "http://127.0.0.1:8000/api/posts/post/1/"
        self.response = self.client.put(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class DeletePostTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a dummy user for authentication purposes
        account = Account.objects.create(
            username="tester", email="tester@gmail.com")
        account.set_password('password123')
        account.save()
        # Create another Account object to act as the author for a Post object
        account = Account.objects.create(
            username="originalwriter", email="originalwriter@gmail.com")
        account.set_password('password123')
        account.save()

        # Create a Post object
        self.url = 'http://127.0.0.1:8000/api/posts/'
        self.data = {
            "body": "The quick brown fox jumped over the lazy dog",
            "author": "1"
        }
        self.login_req = self.client.login(
            username='tester@gmail.com', password='password123')
        self.response = self.client.post(self.url, self.data)

    def test_post_delete_successful(self):
        self.url = "http://127.0.0.1:8000/api/posts/post/1/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_delete_unauthorized(self):
        self.client.logout()
        self.url = "http://127.0.0.1:8000/api/posts/post/1/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(self.response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    # No such Post object
    def test_post_delete_unsuccessful(self):
        self.url = "http://127.0.0.1:8000/api/posts/post/3/delete/"
        self.response = self.client.delete(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
