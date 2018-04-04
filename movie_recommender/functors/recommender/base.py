import booking_system.models as M
from datetime import datetime, timedelta


class BaseRecommender:
    def running(self):
        now = datetime.today()
        # Find all movies with running shows after today. (RMs)
        movie_ids = M.Show.objects.filter(show_time__gt=now).values_list('movie',
                flat=True).distinct()
        movies = list(map(lambda x: M.Movie.objects.get(pk=x), movie_ids))
        return movies

    def local(self, city_id):
        now = datetime.today()
        delta = timedelta(days=-14)
        last_week = now + delta
        city = M.City.objects.get(id=city_id)
        movie_ids = M.Show.objects.filter(screen__theater__location__city=city).values_list('movie', flat=True).distinct()
        movies = list(map(lambda x: M.Movie.objects.get(pk=x), movie_ids))
        return movies
