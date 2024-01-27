from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('first_name', 'admin')
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    CHOICES = [('E', 'Employee'),
               ('T', 'Technical manager'),
               ('M', 'Manager')]
    groups = models.ManyToManyField(Group, related_name='users', db_index=True, blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='users', db_index=True, blank=True)
    role = models.CharField(max_length=1, choices=CHOICES)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def save(self, *args, **kwargs):
        # self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}//{self.id}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'