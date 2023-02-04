from django.db import models  # noqa

# Create your models here.


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
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
            email:
            password:
            **extra_fields: using this arbitrary keyword args option to
                        accomodate any additional user fields in future

        Returns:

        """

        # with `self.model` we are using method associated
        # with default user model
        # as we are deriving from `BaseUserManager`
        user = self.model(email=email, **extra_fields)

        # best practice to hash password using super class method `set_password`
        user.set_password(password)

        # it is best practice to pass `using=self._db`
        # when we are using multiple databases
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in application"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # overrides the default user field from base class
