from dataclasses import fields
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from core import settings



class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,editable=False,null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


