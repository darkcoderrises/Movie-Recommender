#!/bin/bash

python manage.py mlens --path seed/movielens
python manage.py rebuild_index
python manage.py build_similar
