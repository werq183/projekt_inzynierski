from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()


class AI(models.Model):
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=100)
    link = models.URLField()


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Subject(models.Model):
    title = models.CharField(max_length=100)


class Image(models.Model):
    style = models.ForeignKey(Artist, on_delete=models.CASCADE)
    ai = models.ForeignKey(AI, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


