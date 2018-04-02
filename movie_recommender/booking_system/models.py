from django.db import models
from django.contrib.auth.models import User
#import datetime


class CastType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Language(models.Model):
    lang = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.lang
    
class StatusType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class CrewProfile(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    age = models.IntegerField(default=0)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    link = models.TextField(default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre


class UserProfile(User):
    #dob = models.DateField(default=datetime.date.today)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    phone = models.CharField(default="", max_length=10)
    genre_pref = models.ManyToManyField(Genre)

class TheaterOwner(User):
    #age = models.IntegerField(default=0)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    phone = models.CharField(default="", max_length=10)

class Crew(models.Model):
    profile = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    role = models.ForeignKey(CastType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['profile', 'role']

    def __str__(self):
        return self.profile.name

class Movie(models.Model):
    title = models.CharField(max_length=100, default="")
    synopsis = models.TextField(default="")
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    crew = models.ManyToManyField(Crew)
    genres = models.ManyToManyField(Genre)
    

    def __str__(self):
        return self.title


class SeatType(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=100, default="")
    location_lat = models.FloatField(default=0)
    location_long = models.FloatField(default=0)
    seat_types = models.ManyToManyField(SeatType)
    owner=models.ForeignKey(TheaterOwner,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, default="")

    def __str__(self):
        return '{}-{}'.format(self.theater.name, self.identifier)


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    time = models.TimeField()


class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row_id = models.CharField(max_length=3)
    col_id = models.CharField(max_length=5)

    def __str__(self):
        return '{}-{}'.format(self.row_id, self.col_id)


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    show  = models.ForeignKey(Show, on_delete=models.CASCADE)
    type = models.ForeignKey(SeatType, on_delete=models.CASCADE)


class Invoice(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ticket_price = models.FloatField(default=0)
    taxes = models.FloatField(default=0)
    service_charge = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    status = models.ForeignKey(StatusType, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    description = models.TextField(default="")

