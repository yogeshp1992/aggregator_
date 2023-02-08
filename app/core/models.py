from django.db import models  # noqa

# Create your models here.


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

###############################################################
# TOPIC: customizing authentication and user model in django  #
###############################################################
"""
How to customize default django user model and authentication?

Refer - 
https://docs.djangoproject.com/en/4.1/topics/auth/customizing

REFER FULL EXAMPLE HERE -
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example


additional notes ::


"""
###############################################################


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email: str, password: str = None, **extra_fields):
        """

        Args:
            email: will be new default instead of `username`
            password: we will be using `set_password` method to encrypt password
            **extra_fields: using this arbitrary keyword args option to
                        accomodate any additional user fields in future

        Returns:

        """

        if not email:
            raise ValueError("Email field can NOT be blank")

        if len(password) < 5:
            raise ValueError("Password is too short")

        # with `self.model` we are using method associated
        # with default user model
        # as we are deriving from `BaseUserManager`
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # TODO - refer normalize_email method -
        # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email

        # best practice to hash password using super class method `set_password`
        user.set_password(password)

        # it is best practice to pass `using=self._db`
        # when we are using multiple databases
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Whenever we call `python manage.py createsuperuser`, django looks for
        this method.

        Args:
            email:
            password:
            **extra_fields:

        Returns:

        """

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in application"""

    email = models.EmailField(max_length=255, unique=True)
    # TODO
    # apply migrations after every time you change your model
    # email = models.EmailField(max_length=255, unique=True, blank=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"  # overrides the default user field from base class
