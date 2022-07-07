#!/bin/bash


ADMIN_USERNAME="$1"
ADMIN_PASSWORD="$2"
DB_NAME="$3"
DP_PATH="$4"
HOST="$5"
PORT="$6"
DP_FILE="${DB_NAME}.dump"

/opt/dmdbms/bin/dexpdp $ADMIN_USERNAME/$ADMIN_PASSWORD@$HOST:$PORT DIRECTORY=$DP_PATH  FILE=$DP_FILE owner=$DB_NAME
