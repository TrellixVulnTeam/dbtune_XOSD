#!/bin/bash


USERNAME="$1"
PASSWORD="$2"
DB_NAME="$3"
DP_PATH="$4"
DP_FILE="${DB_NAME}.dump"

/opt/dmdbms/bin/dexp $USERNAME/$PASSWORD DIRECTORY=$DP_PATH  FILE=$DP_FILE owner=$DB_NAME
