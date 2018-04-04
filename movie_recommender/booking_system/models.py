from django.db import models
from django.contrib.auth.models import User


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, default=0)
    phone = models.CharField(default="", max_length=10)
    genre_pref = models.ManyToManyField(Genre)

    def __str__(self):
        return self.user.__str__()


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
    release_date = models.DateField()
    tagline = models.TextField(default="")
    imdb_id = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.title


class SeatType(models.Model):
    name = models.CharField(max_length=100, default="")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, default="")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location_lat = models.FloatField(default=0)
    location_long = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=100, default="")
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, default="")

    def __str__(self):
        return '{}-{}'.format(self.theater.name, self.identifier)

    class Meta:
        unique_together = ['theater', 'identifier']


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        unique_together = ['movie', 'screen', 'show_time']


class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row_id = models.CharField(max_length=3)
    col_id = models.CharField(max_length=5)
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.row_id, self.col_id)

    class Meta:
        unique_together = ['row_id', 'col_id', 'screen']


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)


class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                   primary_key=True)
    ticket_price = models.FloatField(default=0)
    taxes = models.FloatField(default=0)
    service_charge = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    status = models.ForeignKey(StatusType, on_delete=models.CASCADE, default=0)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    description = models.TextField(default="")

    class Meta:
        unique_together = ['user', 'movie']


class AggregateRating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    average = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)


class Similar(models.Model):
    query = models.ForeignKey(Movie, on_delete=models.CASCADE,
            related_name='%(class)s_query')
    similar_to = models.ForeignKey(Movie, on_delete=models.CASCADE,
            related_name='%(class)s_similar_to')

    rank = models.FloatField(default=0)

    class Meta:
        unique_together = ['query', 'similar_to']


class PredictedRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return '{} : {} : {}'.format(self.user.username, self.movie.title,
                self.rating)
