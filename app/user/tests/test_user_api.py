"""Tests the user API

# Endpoints

- `/api/user/create`
- `POST`: To create new user

- `/api/user/token/`
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

    def test_retrive_user_unauthorized(self):
        """Test authentication is required for the user"""

        res = self.client.get("/api/user/me/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    @staticmethod
    def create_user(**params):
        """returns user from whichever default user model"""

        return get_user_model().objects.create_user(**params)

    def setUp(self) -> None:
        self.user = self.create_user(
            email="test@example.com",
            password="pasword@213",
            name="Test name"
        )
        self.client = APIClient()

        # We are using `force_authenticate` function to set authentication flag
        # to True. We don't want to create token and authenticate user under
        # each test case. So we have handled authentication part over here.
        # So any subsequent request using self.client to private API
        # endpoints will have an authenticated user.
        self.client.force_authenticate(user=self.user)

    def test_retrive_user_profile(self):
        """Test retrieving user information with valid token"""

        res = self.client.get("/api/user/me/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        """Test updating the user profile for an authenticate user"""

        payload = {"name": "updated name", "password": "password@321"}
        res = self.client.patch("/api/user/me/", payload)
        self.assertEqual(self.user.name, payload.get("name"))








