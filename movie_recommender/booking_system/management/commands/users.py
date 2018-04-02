from django.core.management.base import BaseCommand
import booking_system.models as M
from datetime import datetime
import pandas as pd
import funcy as fy
import random 
import numpy

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            help='File path',
        )

    def handle(self, *args, **options):
        self.seed(options['path'])

    def get(self, Model, **params):
        try:
            instance = Model.objects.get(**params)
        except exceptions.ObjectDoesNotExist:
            instance = Model.objects.create(**params)
            instance.save()
        return instance

    def _gender(self, name):
        return self.get(M.Gender, name=name)

    def _seed_user_profile(self):
        M.UserProfile.objects.all().delete()
        _age = 23
        phones = ["0123456789", "1234567890", "2345678901"]#, "3456789012", "4567890123"]
        usernames = ['Harshil', 'Jerin', 'Mandar']
        passwords = ['Harshil', 'Jerin', 'Mandar']
        gen = "Male"
        genre_pref = ["Sci-Fi", "Fantasy"]
        _genre_pref = [M.Genre.objects.get(genre=g) for g in genre_pref]
        _gender = M.Gender.objects.get(name=gen)
        #creating 3 users
        for i in range(3):
            _user_profile = M.UserProfile.objects.create(gender=_gender, age=_age, phone=phones[i], username=usernames[i], password=passwords[i])
            _user_profile.genre_pref.set(_genre_pref)
            _user_profile.save()

    def seed(self):



