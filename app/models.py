from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(default="", upload_to='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Artysta'
        verbose_name_plural = 'Artyści'
        ordering = ['first_name', 'last_name']


class AI(models.Model):
    name = models.CharField(max_length=50)
    creator = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'AI'
        verbose_name_plural = 'AI'
        ordering = ['name']


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galerie'
        ordering = ['name']


class Subject(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Temat'
        verbose_name_plural = 'Tematy'
        ordering = ['title']


class Image(models.Model):
    style = models.ForeignKey(Artist, on_delete=models.CASCADE)
    ai = models.ForeignKey(AI, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    photo = models.ImageField(default="", upload_to='./images')

    def __str__(self):
        return f"{self.photo.name}"

    class Meta:
        verbose_name = 'Obraz'
        verbose_name_plural = 'Obrazy'
        ordering = ['photo']

