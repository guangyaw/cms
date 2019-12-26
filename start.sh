#!/bin/sh


if ps ax | grep '/home/guangyaw/virtualenv/public_django/cms/3.7/bin/python3.7_bin manage.py qcluster'
then
    echo "qcluster service running, everything is fine"
else
    echo "qcluster is not running"
    source /home/guangyaw/virtualenv/public_django/cms/3.7/bin/activate && cd /home/guangyaw/public_django/cms
    python manage.py qcluster&
fi
