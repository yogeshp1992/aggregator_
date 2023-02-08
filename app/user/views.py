"""
Views for the user API
"""

from rest_framework import generics
from .serializers import UserSerializer, AuthTokenSerializer


# TODO refer - TOPIC: using ready-made functionality available in DRF
# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens

from rest_framework.authtoken.views import ObtainAuthToken

# from django.contrib.auth.tokens import default_token_generator


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new authentication token for new user"""

    serializer_class = AuthTokenSerializer






