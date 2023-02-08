"""Tests the user API

# Endpoints

- `/user/create`
- `POST`: To create new user

- `/user/token/`
- `POST`: To get token

- `/user/me`
- `PUT/PATCH`: To modify user data

"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


class PublicUserApiTests(TestCase):
    """Tests the public features of user API"""

    @staticmethod
    def create_user(**params):
        """returns user from whichever default user model"""

        return get_user_model().objects.create_user(**params)

    def setUp(self) -> None:
        """Instantiate test application"""

        self.client = APIClient()
        # NOTE - if we create test data here, it is called as `test fixture`

    def test_create_user_success(self):
        """
        Test creating user is successful (/user/create)
        """

        payload = {
            "email": "test@example.com",
            "password": "password@321",
            "name": "Test Name",
        }

        res = self.client.post("/api/user/create/", payload)
        self.assertEqual(res.status_code, 201)

    def test_create_user_short_password(self):
        """
        Test creating user is successful (/user/create)
        """

        payload = {"email": "test@example.com", "password": "pwd", "name": "Test Name"}
        res = self.client.post("/api/user/create/", payload)
        self.assertEqual(res.status_code, 400)

    def test_user_with_email_exists_error(self):
        """Test error returned if user email already exists"""

        payload = {
            "email": "test@example.com",
            "password": "password@123",
            "name": "Test Name"
        }
        # step 1: create user using ORM
        self.create_user(**payload)

        # step 2: create user using API
        res = self.client.post("/api/user/create/", payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test generates token for valid user credentials

        /api/user/token

        """

        payload = {
            "email": "test@example.com",
            "password": "newuserpassword@123",
            "name": "Test Name"
        }
        self.create_user(**payload)

        res = self.client.post("/api/user/token/", payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)





