#
# OtterTune - credentials_TEMPLATE.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
"""
Private/custom Django settings for the OtterTune project.

"""
# pylint: disable=invalid-name

# ==============================================
# SECRET KEY CONFIGURATION
# ==============================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ADD ME!!'

# ==============================================
# DATABASE CONFIGURATION
# ==============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ottertune',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '192.168.144.152',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES',innodb_strict_mode=1",
        },
    }
}

# ==============================================
# DEBUG CONFIGURATION
# ==============================================

# Can override the DEBUG setting here
DEBUG = False

# 作用就是自动在网址结尾加'/'
# ==============================================
# MANAGER CONFIGURATION
# ==============================================

# Admin and managers for this project. These people receive private
# site alerts.
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# ==============================================
# GENERAL CONFIGURATION
# ==============================================

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']
