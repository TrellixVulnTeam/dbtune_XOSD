import os
from os.path import realpath, dirname, join
from pathlib import Path

# ==========================================================
#  HOST LOGIN
# ==========================================================
# Valid values= local, remote, docker or remote_docker
HOST_CONN = 'remote_docker'

# ==========================================================
#  DATABASE OPTIONS
# ==========================================================
DB_TYPE = 'dm'

# Database version
DB_VERSION = '8.0'

# Name of the database
DB_NAME = 'TRAIN'

# Database username
DB_USER = 'TRAIN'

# Password for DB_USER
DB_PASSWORD = '123456789'

# Database admin username (for tasks like restarting the database)
# DM库配置
ADMIN_USER = 'SYSCDB'
ADMIN_PWD = 'Dameng8888'

# Database host address
DB_HOST = '$DB_HOST'

# Database port
DB_PORT = '5236'

# If set to True, DB_CONF file is mounted to database container file
# Only available when HOST_CONN is docker or remote_docker
DB_CONF_MOUNT = False

# Path to the configuration file on the database server
# If DB_CONF_MOUNT is True, the path is on the host server, not docker
DB_CONF = '/opt/dmdbms/dm.ini'
REMOTE_DB_CONF = '/opt/dmdbms/data/DAMENG/dm.ini'

# Base config settings to always include when installing new configurations
BASE_DB_CONF = None

# Name of the device on the database server to monitor the disk usage, or None to disable
DATABASE_DISK = '/'

# Set this to a different database version to override the current version
OVERRIDE_DB_VERSION = None

# 数据库实例ID
# UPLOAD_CODE = '$DB_INSTANCE_ID'
DB_POD_NAME = '$DB_POD_NAME'

# ==========================================================
#  DRIVER OPTIONS
# ==========================================================
# Path to this driver
DRIVER_HOME = dirname(Path(__file__).resolve().parent)

# Path to the directory for storing results
RESULT_DIR = join(DRIVER_HOME, 'results')

# Set this to add user defined metrics
ENABLE_UDM = True

# Path to the User Defined Metrics (UDM), only required when ENABLE_UDM is True
UDM_DIR = os.path.join(DRIVER_HOME, 'userDefinedMetrics')

# Path to temp directory
TEMP_DIR = '/tmp/driver'

# Path to the directory for storing database dump files
DB_DUMP_DIR = os.path.join(DRIVER_HOME, 'dumpfiles')

# Reload the database after running this many iterations
RELOAD_INTERVAL = 10

# The maximum allowable disk usage percentage. Reload the database
# whenever the current disk usage exceeds this value.
MAX_DISK_USAGE = 90

# Execute this many warmup iterations before uploading the next result
# to the website
WARMUP_ITERATIONS = 0

# Let the database initialize for this many seconds after it restarts
RESTART_SLEEP_SEC = 20



# ==========================================================
#  WEBSITE OPTIONS
# ==========================================================
# OtterTune website URL
WEBSITE_URL = 'http://localhost:8000'

# Code for uploading new results to the website
UPLOAD_CODE = '$UPLOAD_CODE'

# ==========================================================
#  CONTROLLER OPTIONS
# ==========================================================
# Controller observation time, OLTPBench will be disabled for
# monitoring if the time is specified
CONTROLLER_OBSERVE_SEC = 100

# Path to the controller directory
CONTROLLER_HOME = DRIVER_HOME + '/../controller'

# Path to the controller configuration file
CONTROLLER_CONFIG = os.path.join(CONTROLLER_HOME, 'config/{}_{}_config.json'.format(DB_TYPE, UPLOAD_CODE))

# ==========================================================
#  BENCH OPTIONS
# ==========================================================
# oltpbench or sysbench
BENCH_TYPE = 'sysbench'

# Path to SYSBENCH directory
SYSBENCH_HOME = os.path.expanduser('/home/sysbench')

# ==========================================================
#  LOGGING OPTIONS
# ==========================================================
LOG_LEVEL = 'DEBUG'

# Path to log directory
LOG_DIR = os.path.join(DRIVER_HOME, 'log')

# Log files
DRIVER_LOG = os.path.join(LOG_DIR, UPLOAD_CODE, 'driver.log')
BENCH_LOG = os.path.join(LOG_DIR, UPLOAD_CODE, 'bench.log')
CONTROLLER_LOG = os.path.join(LOG_DIR, UPLOAD_CODE, 'controller.log')

