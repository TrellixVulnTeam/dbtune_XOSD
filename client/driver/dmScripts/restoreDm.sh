#!/bin/sh

USERNAME="$1"
PASSWORD="$2"
DB_NAME="$3"
DP_FILE="$4"

/opt/dmdbms/bin/dimp $USERNAME/$PASSWORD file=$DP_FILE owner=$DB_NAME ignore=y
