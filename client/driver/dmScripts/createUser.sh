#!/bin/bash

ADMIN_USERNAME="$1"
ADMIN_PASSWORD="$2"
USERNAME="$3"
PASSWORD="$4"
HOST="$5"
PORT="$6"

/opt/dmdbms/bin/disql $ADMIN_USERNAME/$ADMIN_PASSWORD@$HOST:$PORT <<EOF
  CREATE USER "$USERNAME" IDENTIFIED BY "$PASSWORD" limit failed_login_attemps 3, password_lock_time 1, password_grace_time 10;
  grant "DBA","PUBLIC","VTI","SOI" to "$USERNAME";
  grant ALTER DATABASE,RESTORE DATABASE,CREATE USER,ALTER USER,DROP USER,CREATE ROLE,CREATE SCHEMA,CREATE TABLE,CREATE VIEW,CREATE PROCEDURE,CREATE SEQUENCE,CREATE TRIGGER,CREATE INDEX,CREATE CONTEXT INDEX,BACKUP DATABASE,CREATE LINK,CREATE REPLICATE,CREATE PACKAGE,CREATE SYNONYM,CREATE PUBLIC SYNONYM,ALTER REPLICATE,DROP REPLICATE,DROP ROLE,ADMIN ANY ROLE,ADMIN ANY DATABASE PRIVILEGE,GRANT ANY OBJECT PRIVILEGE,INSERT TABLE,INSERT ANY TABLE,UPDATE TABLE,UPDATE ANY TABLE,DELETE TABLE,DELETE ANY TABLE,SELECT TABLE,SELECT ANY TABLE,REFERENCES TABLE,REFERENCES ANY TABLE,GRANT TABLE,GRANT ANY TABLE,INSERT VIEW,INSERT ANY VIEW,UPDATE VIEW,UPDATE ANY VIEW,DELETE VIEW,DELETE ANY VIEW,SELECT VIEW,SELECT ANY VIEW,GRANT VIEW,GRANT ANY VIEW,CREATE SESSION to "$USERNAME";
quit
EOF

