from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not phone:
            raise ValueError('Phone number is required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique= True)
    phone = models.CharField(_('phone number'), max_length= 20, unique= True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
