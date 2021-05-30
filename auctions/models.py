from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField , IntegerField , TextField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    details = models.TextField(default='')
    price = models.IntegerField()
    owner = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    item = models.ForeignKey(Listing , on_delete=models.CASCADE , related_name="comments")
    content = models.TextField(default='')

    def __str__(self):
        return f"{self.item.title} : {self.content}"

