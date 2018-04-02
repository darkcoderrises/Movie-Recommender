from surprise import Reader, Dataset, SVD, evaluate
import booking_system.models as M
from django_pandas.io import read_frame
import pandas as pd

class CFRecommender:
    def top(self, count):
        pass

    def compute(self):
        reader = Reader()
        ratings = M.Review.objects.all().defer('description')
        ratings = read_frame(ratings, fieldnames=['user__id', 'movie__id', 'rating'])
        data = Dataset.load_from_df(ratings[['user__id', 'movie__id', 'rating']], reader)
        data.split(n_folds=5)
        svd = SVD()
        evaluate(svd, data, measures=['RMSE', 'MAE'])
        trainset = data.build_full_trainset()
        svd.train(trainset)
        for user in ratings['user__id']:
            for movie in ratings['movie__id']:
                print(svd.predict(user, movie, 3))




