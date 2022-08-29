#!/bin/bash

addr_port="0.0.0.0:8000"

# Wait for backend connection
/bin/bash wait-for-it.sh

## Needs a connection to a DB so migrations go here
#python3 manage.py makemigrations website
python3 manage.py migrate
python3 manage.py createuser admin admin --superuser
python3 manage.py stopcelery
python3 manage.py startcelery
#celery -A celery flower

echo ""
echo "-=------------------------------------------------------"
echo " Starting the web server on '$addr_port'..."
echo "-=------------------------------------------------------"
python3 manage.py runserver "$addr_port"
