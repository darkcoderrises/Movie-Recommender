import pandas as pd

ratings = pd.read_csv('ratings_small.csv')
movies = pd.read_csv('movies_metadata.csv.small')
names = pd.read_csv('names_small.csv.small')

ratings['id'] = ratings['userId']
x = pd.merge(ratings, names, on='id')
x['id'] = ratings['movieId']
y = pd.merge(x, movies, on='id')
print(y.head())
ratings_small = y[ratings.columns.values]
print(ratings_small)
ratings_small.to_csv('ratings_small.csv.small', index=False)
