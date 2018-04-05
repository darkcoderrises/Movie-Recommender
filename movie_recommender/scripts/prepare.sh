#!/bin/bash

python manage.py mlens --path seed/movielens
python manage.py seed --path seed/location.csv,seed/theatre_location.csv
python manage.py rebuild_index
python manage.py build_similar
