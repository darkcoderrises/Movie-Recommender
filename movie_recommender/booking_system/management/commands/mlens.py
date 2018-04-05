from django.core.management.base import BaseCommand
import django.core.exceptions as exceptions
import django.db as db
import booking_system.models as M
from datetime import datetime
import pandas as pd
import funcy as fy
import random 
import numpy
from . import mldt

from ast import literal_eval
from pprint import pprint

gender_map = dict([
    (0, "Male"),
    (1, "Female"),
    (2, "Male")
])




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            help='File path',
        )

        parser.add_argument('--debug', dest='debug', action='store_true')
        parser.add_argument('--no-debug', dest='debug', action='store_false')
        parser.set_defaults(debug=True)


    def handle(self, *args, **options):
        self.debug = options['debug']
        self.seed(options['path'])


    def seed(self, path):
        data = mldt.load(path, self.debug)
        self.prototype(data)

    def get(self, Model, **params):
        try:
            instance = Model.objects.get(**params)
        except exceptions.ObjectDoesNotExist:
            instance = Model.objects.create(**params)
            instance.save()
        return instance



    def mapping(self, _m, df):
        _d = {}
        for key in _m:
            _d[key] = df[_m[key]]
        return _d

    def _movie(self, mf): 
        _mapping = {
           "id": "id",
           "synopsis": "overview", 
           "tagline": "tagline" ,
           "title": "title",
           "release_date": "release_date",
           "imdb_id": "imdb_id",
           "language": "original_language",
        }


        params = self.mapping(_mapping, mf)
        params["language"] = self.get(M.Language,
                lang=params["language"])
        movie = self.get(M.Movie, **params)
        self._aggregate_rating(movie, mf)
        self._genres(movie, mf)
        return movie

    def _aggregate_rating(self, movie, mf):
        _mapping = {
                "average": "vote_average",
                "count": "vote_count",
                "popularity": "popularity"
        }
        params = self.mapping(_mapping, mf)
        rating = self.get(M.AggregateRating, **params, movie=movie)
    

    def _genre(self, genre):
        return self.get(M.Genre, genre=genre)

    def _cast(self, cf):
        pass

    def _language(self, lang):
        return self.get(M.Language, lang=lang)

    def _gender(self, name):
        return self.get(M.Gender, name=name)

    def _crew_profile(self, profile):
        _id = profile["gender"]
        _gender = self._gender(gender_map[_id])
        return self.get(M.CrewProfile, 
            name=profile["name"], gender=_gender)

    def _add_movie_crew(self, crew, movie):
        try:
            movie.crew.add(crew)
            movie.save()
        except exceptions.ObjectDoesNotExist:
            raise
            print("Deferring movie!")

    def _cast_type(self, name):
        return self.get(M.CastType, name=name)

    def _crew(self, _profile, cast_type):
        return self.get(M.Crew, profile=_profile, role=cast_type)

    def _user(self, user):
        keys = ['first_name', 'last_name', 'username']
        params = self.mapping(dict(zip(keys, keys)), user)
        gender = self.get(M.Gender, name=user['gender'])
        user_obj = self.get(M.User, **params)
        return self.get(M.UserProfile, user=user_obj, gender=gender)

    def _genres(self, movie, mf):
        serialized_genre = mf["genres"]
        genres = literal_eval(serialized_genre)
        _genres = []
        for genre in genres:
            _genre = self._genre(genre["name"])
            _genres.append(_genre)
        movie.genres.set(_genres)


    def _casts(self, cast, movie):
        cast = literal_eval(cast)
        cast_type = self._cast_type("Actor")
        for profile in cast:
            _profile = self._crew_profile(profile)
            _crew = self._crew(_profile, cast_type)
            self._add_movie_crew(_crew, movie)

    def _add_rating(self, rating):
        uid = rating['userId'].astype(int)
        mid = rating['movieId'].astype(int)
        movie = self.get(M.Movie, id=mid)
        user = self.get(M.UserProfile, id=uid)
        user_obj.set_password('letmein')
        user_obj.save()
        _rating = self.get(M.Review, user=user, movie=movie, 
                rating=rating["rating"])
        print(uid, mid, rating["rating"]) 

    def prototype(self, data):
        user = data["names_small"]

        def wrapped(iterator):
            limit = 50
            if self.debug: return fy.take(limit, iterator)
            return iterator

        for i, user in wrapped(user.iterrows()):
            _user = self._user(user)
            print(_user)

        movies = data["movies_metadata"]
        credits = data["credits"]

        iterator = zip(movies.iterrows(), credits.iterrows())
        for pack in wrapped(iterator):
            (i, movie), (j, credit) = pack 
            _movie = self._movie(movie)
            print(i, movie["title"], _movie.id, movie["id"])
            cast, crew, _id = credit
            self._casts(cast, _movie)
            director = mldt.director(literal_eval(crew))
            if director is not None:
                _profile = self._crew_profile(director)
                cast_type = self._cast_type("Director")
                _crew = self._crew(_profile, cast_type)
                self._add_movie_crew(_crew, _movie)

        ratings = data["ratings_small"]
        for i, rating in wrapped(ratings.iterrows()):
            self._add_rating(rating)

