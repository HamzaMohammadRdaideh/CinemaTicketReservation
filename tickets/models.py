from django.db import models

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
    guset = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservation')        


    def __str__(self):
        return self.guset