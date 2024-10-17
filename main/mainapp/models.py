# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
  def create_user(self, email=None, mobile=None, password=None, **extra_fields):
      if not email and not mobile:
          raise ValueError('The Email or Mobile number must be set')
      email = self.normalize_email(email)
      user = self.model(email=email, mobile=mobile, **extra_fields)
      if password:
          user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, mobile, password=None, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)

      return self.create_user(email, mobile, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True, null=True, blank=True)
  mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
  username = models.CharField(max_length=150, unique=True, null=True, blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'  # or 'mobile', depending on your primary login method
  REQUIRED_FIELDS = []

  def __str__(self):
      return self.email or self.mobile