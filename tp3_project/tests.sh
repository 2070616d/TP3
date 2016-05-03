#!/bin/bash
source project/bin/activate
flake8 --ignore=F403,E501 stove > flake8res
pepper8 -o styleres.html flake8res
rm flake8res
coverage run --source='stove' manage.py test
ret=$?
coverage html
exit $ret
