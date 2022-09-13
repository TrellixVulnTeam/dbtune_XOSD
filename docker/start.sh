#!/bin/bash

addr_port="0.0.0.0:8000"

/bin/bash install.sh
# Wait for backend connection
source wait-for-it.sh

## Needs a connection to a DB so migrations go here
#python3 manage.py makemigrations website
if [ $IS_DB_INIT -lt 1 ]; then
  python3 manage.py migrate
  python3 manage.py createuser admin admin --superuser
fi

#python3 manage.py initmq
python3 manage.py stopcelery
nohup /bin/bash check-celery.sh >/dev/null 2>&1 &
#python3 manage.py startcelery
#celery -A celery flower

echo ""
echo "-=------------------------------------------------------"
echo " Starting the web server on '$addr_port'..."
echo "-=------------------------------------------------------"
python3 manage.py runserver "$addr_port" --noreload
