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

from rest_framework.test import APIClient


class PublicUserApiTests(TestCase):
    """Tests the public features of user API"""

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
            "name": "Test Name"
        }

        res = self.client.post("/api/user/create/", payload)
        self.assertEqual(res.status_code, 201)

    def test_create_user_short_password(self):
        """
        Test creating user is successful (/user/create)
        """

        payload = {
            "email": "test@example.com",
            "password": "pwd",
            "name": "Test Name"
        }
        res = self.client.post("/api/user/create/", payload)
        self.assertEqual(res.status_code, 400)

