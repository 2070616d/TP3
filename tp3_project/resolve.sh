#!/bin/bash
virtualenv --python=/usr/local/bin/python2.7 project
source project/bin/activate
pip install Django==1.9.4
pip install flake8
pip install jinja2
pip install pepper8
pip install coverage
pip install python-social-auth
pip install easy_thumbnails
pip install django-image-cropping
