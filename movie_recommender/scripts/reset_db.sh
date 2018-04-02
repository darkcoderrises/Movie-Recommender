#!/bin/bash
rm db.sqlite3
rm -r booking_system/migrations/*
touch booking_system/migrations/__init__.py

python manage.py makemigrations
python manage.py migrate
