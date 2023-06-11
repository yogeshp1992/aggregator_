"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from rest_framework import serializers


# TODO - TOPIC - (DRF ModelSerializers), refer
# https://www.django-rest-framework.org/tutorial/1-serialization/#using-modelserializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "email": {"min_length": 5},
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""

        return get_user_model().objects.create_user(**validated_data)
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, data):
        """validate and authenticate the user"""

        email = data.get("email")
        if email.isupper():
            raise serializers.ValidationError("Email is not as per standards")

        password = data.get("password")

        # this is just to validate
        # if user name and password exists in the database
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            msg = "Unable to authenticate user with given credentials"
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data

