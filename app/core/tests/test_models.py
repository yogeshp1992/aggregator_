"""
Test the models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """testing of models"""

    def test_create_user_with_email_as_default(self):
        """test creating a user with just email field and password alone"""

        email = "test@example.com"
        password = "test@pass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)

