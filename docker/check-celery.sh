#!/bin/bash

while true
do
   celery_status=$(python3 manage.py celery inspect ping)
   if [[ $celery_status != *"pong"* ]]; then
     python3 manage.py startcelery
   fi

   sleep 5
done



