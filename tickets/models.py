from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings #Default user model

# Create your models here.

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie_name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.hall


class Guest(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservation')        


    def __str__(self):
        return str(self.guest)


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def token_create(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)