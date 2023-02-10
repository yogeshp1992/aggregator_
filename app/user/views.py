"""
Views for the user API
"""

from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from .serializers import UserSerializer, AuthTokenSerializer


# TODO refer - TOPIC: using ready-made functionality available in DRF
# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens

from rest_framework.authtoken.views import ObtainAuthToken

# from django.contrib.auth.tokens import default_token_generator


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new authentication token for new user"""

    serializer_class = AuthTokenSerializer


class ManageUserView(RetrieveUpdateAPIView):
    """
    get
    patch
    put

    TODO - TOPIC (generic views RetriveUpdateView)
    https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdateapiview
    """

    serializer_class = UserSerializer

    # checking http header for authentication token  (authentication)
    authentication_classes = [authentication.TokenAuthentication]

    # allow users only when token is valid   (authorized)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrive user and return authenticated user information"""

        return self.request.user








