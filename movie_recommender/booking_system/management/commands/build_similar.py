from django.core.management.base import BaseCommand
import django.core.exceptions as exceptions
import django.db as db
import booking_system.models as M
from datetime import datetime
import pandas as pd
import funcy as fy
import random 
import numpy
from ast import literal_eval
from pprint import pprint
from functors.recommender import CBRecommender

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        R = CBRecommender()
        R.compute()
        print("Done")



