#!/bin/bash

ps -ef | grep "mysql" | grep -v grep | tr -s " " | cut -d" " -f2 | xargs kill -9

nohup mysqld_safe --defaults-file=/home/mysql/conf/my.cnf >/dev/null 2>&1 &
if [ "$?" -ne 0 ]; then
  echo "mysql service not ready..."
  exit 0
fi

ready() {
  a=`netstat -nlp | grep 3306 | wc -l`
  if [ "$a" -gt "0" ];then
      return 0
  else
      return 1
  fi
}


counter=1
max_counter=30
while ! ready; do
  counter=$(expr $counter + 1)

  if [ $counter -gt $max_counter ]; then
    echo "ERROR: Could not connect to mysql; Exiting..."
    exit 1
  fi
  sleep 1
done

db_password='MTIzNDU2NzgK'
pwd=$(echo $db_password | base64 -d)

# 本地首次使用sock文件登录mysql是不需要密码的
mysql -S /home/mysql/tmp/mysqld.sock <<EOF
use mysql;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$pwd';
grant all privileges on *.* to 'root'@'localhost';
# 刷新权限表
FLUSH PRIVILEGES;
CREATE USER 'root'@'%' IDENTIFIED BY '$pwd';
# 修改密码
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '$pwd';
grant all privileges on *.* to 'root'@'%';
# 刷新权限表
FLUSH PRIVILEGES;
select host,user,authentication_string from mysql.user;
create database db_tune default character set utf8mb4 collate utf8mb4_unicode_ci;
EOF

# 登录sock软连接到tmp目录
ln -fs /home/mysql/tmp/mysqld.sock /tmp/mysql.sock

echo "-=------------------------------------------------------"
echo "-=---------------  数据库列表： ---------------------------"
echo "$(mysql --host="localhost" --protocol TCP -u"root" -p"$pwd" -e "show databases;")"
echo "-=------------------------------------------------------"
