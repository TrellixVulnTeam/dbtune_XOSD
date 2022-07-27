#!/bin/bash


ADMIN_USERNAME="$1"
ADMIN_PASSWORD="$2"
DB_NAME="$3"
DP_PATH="$4"
HOST="$5"
PORT="$6"
DP_FILE="${DB_NAME}.dump"

/opt/dmdbms/bin/dexp $ADMIN_USERNAME/$ADMIN_PASSWORD@$HOST:$PORT DIRECTORY=$DP_PATH  FILE=$DP_FILE owner=$DB_NAME DUMMY=Y

# 忽略命令执行内部的警告
if [ $? -eq 2 ]; then
     echo "succeed"
fi
