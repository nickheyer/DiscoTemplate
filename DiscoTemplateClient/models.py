from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

import os

class Configuration(models.Model):
    prefix_keyword = models.CharField("Chat-Prefix For Requests", max_length=255, null=True, default="!dt")
    discord_token = models.CharField("Discord Token", max_length=255, null=True, default="")

    session_timeout = models.IntegerField("Session Timeout", null=True, default=60)

    is_verbose_logging = models.BooleanField("Verbose logging in console", default=False)
    is_debug = models.BooleanField("Send Debug Message On Error", default=False)

class State(models.Model):
    discord_state = models.BooleanField(default=False)
    app_state = models.BooleanField(default=True)
    current_activity = models.CharField(max_length=255, default="Offline")
    host_url = models.CharField(max_length=128, default='0.0.0.0:5454')


class ErrLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(max_length=2048, default="Error Occured")


class EventLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(max_length=2048, default="Event Occured")


class DiscordServer(models.Model):
    server_name = models.CharField(max_length=255, null=True)
    server_id = models.CharField(max_length=255, null=True)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    added = models.DateTimeField(default=now, editable=True, )
    is_admin = models.BooleanField(default=False)
    is_server_restricted = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True, null=False)
    discord_servers = models.ManyToManyField(DiscordServer, related_name="users", blank=True)
    is_additional_settings = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    session_timeout = models.IntegerField(default=60)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app"""
        return True

    def __str__(self):
        return self.username


