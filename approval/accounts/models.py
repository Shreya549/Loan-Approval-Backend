from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta
from datetime import datetime as dtime
from django.conf import settings
from uuid import uuid4

import jwt
import time
import uuid

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
            self, email, fname, lname, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not fname:
            raise ValueError(_('Users must have a first name'))
        if not lname:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            fname=fname,
            lname = lname
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            lname = lname,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']

    objects = UserManager()

    @property
    def token(self):
        dt = dtime.now() + timedelta(days=2)
        token = jwt.encode({
            'id': self.id,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS512')
        return token.decode('utf-8')

    def natural_key(self):
        return (self.fname + " " + self.lname)

    def __str__(self):
        return self.email

