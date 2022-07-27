Website
=======

```text
OLTP-Bench Website is an intermediate between the client's database and OtterTune (DBMS Auto-tuning system).

OLTP-Bench 网站是客户端数据库和 OtterTune（DBMS 自动调整系统）之间的中间体。
```

## Requirements

##### Ubuntu Packages

```
sudo apt-get install python-pip python-dev python-mysqldb rabbitmq-server
```

##### Python Packages

```
sudo pip install -r requirements.txt
```

## Installation Instructions


##### 1. Update the Django settings

Navigate to the settings directory:

```
cd website/settings
```

Copy the credentials template:

```
cp credentials_TEMPLATE.py credentials.py
```

Edit `credentials.py` and update the secret key and database information.

##### 2. Serve the static files

If you do not use the website for production, simply set `DEBUG = True` in `credentials.py`. Then Django will handle static files automatically. 

This is not an efficient way for production. You need to configure other servers like Apache to serve static files in the production environment. ([Details](https://docs.djangoproject.com/en/1.11/howto/static-files/deployment/))

##### 3. Create the MySQL database if it does not already exist

```
mysqladmin create -u <username> -p ottertune

use mysql;
SET GLOBAL validate_password.policy = LOW;
CREATE USER 'root'@'%' IDENTIFIED BY '12345678';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '12345678';

CREATE USER 'ottertune'@'%' IDENTIFIED BY '12345678';
create database ottertune default character set utf8mb4 collate utf8mb4_unicode_ci;
ALTER USER 'ottertune'@'%' IDENTIFIED WITH mysql_native_password BY '12345678';

grant all privileges on *.* to 'root'@'%';
FLUSH PRIVILEGES;
```

##### 4. Migrate the Django models into the database

```
cd /home/zhc/anaconda3/envs/py37-env/
source activate py37-env
#python3 manage.py makemigrations website
python3 manage.py migrate
```

##### 5. Create the super user

```
python3 manage.py createsuperuser
```
    
##### 6. Start the message broker, celery worker, website server, and periodic task

```
sudo rabbitmq-server -detached || systemctl restart rabbitmq-server
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py celery worker --loglevel=info --pool=threads
python3 manage.py celerybeat --verbosity=2 --loglevel=info 
```



##### # 执行：【python3 manage.py celery worker --loglevel=info --pool=threads】报错
```shell
  File "/home/zhc/ottertune/venv/lib/python3/site-packages/celery/concurrency/threads.py", line 13, in <module>
    from .base import apply_target, BasePool
  File "/home/zhc/ottertune/venv/lib/python3/site-packages/celery/concurrency/base.py", line 21, in <module>
    from celery.utils import timer2
  File "/home/zhc/ottertune/venv/lib/python3/site-packages/celery/utils/timer2.py", line 19
    from kombu.async.timer import Entry, Timer as Schedule, to_timestamp, logger
                   ^
SyntaxError: invalid syntax

/usr/local/lib/python3.7/dist-packages/kombu

这是因为在 python 3.7 中将 async 作为了关键字，所以当 py 文件中出现类似 from . import async, base 这类不符合python语法的语句时，Python会报错；
解决方法： 在 celery 官方的提议下，建议将 kombu下的async.py 文件的文件名改成 asynchronous ,然后把引用和这个文件的所有文件的里面的async改为asynchronous
```
https://blog.csdn.net/qq_51236600/article/details/116681098

##### #scipy安装错误及解决（libraries mkl_rt not found）
pip install Cython
apt-get install libopenblas-dev liblapack-dev libatlas-base-dev libblas-dev -y

#### #Django 404 error-page not found
https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail

#### #mysql_config: not found
apt install libmysqlclient-dev


##### # 执行：【python3  manage.py celery worker 】报错
```shell
root@gpu-node1:/home/zhc/ottertune/server/website# python3  manage.py celery worker  --loglevel=info
Running a worker with superuser privileges when the
worker accepts messages serialized with pickle is a very bad idea!

If you really want to continue then you have to set the C_FORCE_ROOT
environment variable (but please think about this before you do).

User information: uid=0 euid=0 gid=0 egid=0

解决:
export C_FORCE_ROOT="true"
```

##### # 登录rabbitmq报错User can only log in via localhost
```shell
找到/rabbitmq_server-3.6.14/ebin下面的rabbit.app文件文件完整内容如下（注意后面的半角句号）：
找到：loopback_users里的<<"guest">>删除。

[{rabbit, [{loopback_users, []}]}]

然后重启
systemctl restart rabbitmq-server.service
```

##### # error in setup command: use_2to3 is invalid.
```shell
在setuptools 58之后的版本已经废弃了use_2to3:

pip install setuptools==57.5.0
```
