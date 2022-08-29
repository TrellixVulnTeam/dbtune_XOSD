import json
import random
import string
from datetime import timedelta
from os import environ as env
import base64

debug = env.get('DEBUG', 'False')
rabbitmq_host = env.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = env.get('RABBITMQ_PORT', '5672')
rabbitmq_user = env.get('RABBITMQ_USER', 'guest')
rabbitmq_pwd = env.get('RABBITMQ_PWD', 'guest')
default_queue = env.get('CELERY_DEFAULT_QUEUE', 'default')
CELERY_APP_QUEUE = env.get('CELERY_APP_QUEUE', 'app')
backend = env.get('BACKEND', 'mysql')
db_name = env.get('DB_NAME', 'db_tune')
db_host = env.get('DB_HOST', 'localhost')
db_port = env.get('DB_PORT', '3306')
db_user = env.get('DB_USER', 'root')
db_pwd = env.get('DB_PASSWORD', 'MTIzNDU2Nzg=')
db_pwd = base64.b64decode(db_pwd).decode('utf-8')

default_opts = {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES',innodb_strict_mode=1",
}
db_opts = env.get('DB_OPTS', default_opts)
bg_run_every = env.get('BG_TASKS_RUN_EVERY', 5)  # minutes

if isinstance(db_opts, str):
    db_opts = json.loads(db_opts) if db_opts else {}

SECRET_KEY = ''.join(random.choice(string.hexdigits) for _ in range(16))
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.' + backend,
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_pwd,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': db_opts,
                }
}

DEBUG = debug

ADMINS = ()
MANAGERS = ADMINS
ALLOWED_HOSTS = ['*']
BROKER_URL = 'amqp://{}:{}@{}:{}//'.format(rabbitmq_user, rabbitmq_pwd, rabbitmq_host, rabbitmq_port)

if bg_run_every is not None:
    # Defines the periodic task schedule for celerybeat
    CELERYBEAT_SCHEDULE = {
        'run-every-{}m'.format(bg_run_every): {
            'task': 'run_background_tasks',
            'schedule': timedelta(minutes=int(bg_run_every)),
        }
    }
