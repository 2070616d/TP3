#!/bin/bash

rm stove/migrations/0*.py
rm tp3_project.db
python manage.py makemigrations stove
python manage.py migrate
python populate_db.py
