from surprise import Reader, Dataset, SVD, evaluate
import booking_system.models as M
from django_pandas.io import read_frame
import pandas as pd
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .base import BaseRecommender

class CFRecommender(BaseRecommender):
    def top(self, user, count):
        movies = self.running()
        bookings = M.Booking.objects.filter(user=user)
        booked_movies = list(map(lambda x: x.show.movie, bookings))
        ratings = M.PredictedRating.objects.filter(user=user,
                    movie__in=movies
                ).order_by('rating'
                ).exclude(movie__in=booked_movies)
        return ratings


    def compute(self):
        reader = Reader()
        ratings = M.Review.objects.all().defer('description')
        ratings = read_frame(ratings, 
                fieldnames=['user__id', 'movie__id', 'rating'])
        data = Dataset.load_from_df(ratings[['user__id', 'movie__id', 'rating']], reader)
        data.split(n_folds=5)
        svd = SVD()
        evaluate(svd, data, measures=['RMSE', 'MAE'])
        trainset = data.build_full_trainset()
        result = []
        gen_dict = lambda **kw: kw
        for user in ratings['user__id'].unique():
            for movie in ratings['movie__id'].unique():
                row = svd.predict(user, movie)
                result.append(row)
        result = pd.DataFrame(result)
        predictions = result.drop(['r_ui', 'details'], axis=1)
        for i, prediction in predictions.iterrows():
            user = M.User.objects.get(pk=prediction['uid'])
            movie = M.Movie.objects.get(pk=prediction['iid'])
            self.set_rating(user, movie, prediction['est'])


    def set_rating(self, user, movie, r):
        try:
            rating = M.PredictedRating.objects.get(user=user, movie=movie)
            rating.rating = r
            rating.save()
        except ObjectDoesNotExist:
            rating = M.PredictedRating.objects.create(user=user, movie=movie,
                    rating=r)
            rating.save()
            



    def special(self):
        movies = self.running()
        running_ratings = M.Review.objects.filter(movie__in=movies
                ).defer('description')

        running_ratings = read_frame(running_ratings, 
                fieldnames=['user__id', 'movie__id', 'rating'])

        # Sample a few old movies. (OMs)
        # Preferably the one the user watched.

        # Find reviewers of running shows, and common old movies.
        # Rs
        # Using (RMs + OMs), build rating dataframe.
        ratings = pd.concat([running_ratings])

