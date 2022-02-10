from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    date = models.DateField()
    age_restriction = models.CharField(max_length=4)
    genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.name

    def rating(self):
        count_reviews = self.reviews.count()
        sum = self.reviews.aggregate(Sum('rate'))['rate__sum']
        try:
            return sum / count_reviews
        except:
            return 0


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    rate = models.IntegerField(default=5)

    def __str__(self):
        return self.movie.name



