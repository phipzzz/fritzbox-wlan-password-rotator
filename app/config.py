import os
import string

def get_bool_value(env, default):
    if env in ['true', 'True']:
        return True
    elif env in ['false', 'False']:
        return False
    else:
        return default

PW_CHARSET_ASCII_LOWERCASE = get_bool_value(os.environ.get('PW_CHARSET_ASCII_LOWERCASE'), True)
PW_CHARSET_ASCII_UPPERCASE = get_bool_value(os.environ.get('PW_CHARSET_ASCII_UPPERCASE'), True)
PW_CHARSET_DIGITS = get_bool_value(os.environ.get('PW_CHARSET_DIGITS'), True)
PW_CHARSET_PUNCTUATION = get_bool_value(os.environ.get('PW_CHARSET_PUNCTUATION'), True)

if PW_CHARSET_PUNCTUATION:
    PW_CHARSET_PUNCTUATION_USE_CUSTOM = get_bool_value(os.environ.get('PW_CHARSET_PUNCTUATION_USE_CUSTOM'), True)
else:
    PW_CHARSET_PUNCTUATION_USE_CUSTOM = False

PW_CHARSET_PUNCTUATION_CUSTOM = os.environ.get('PW_CHARSET_PUNCTUATION_CUSTOM')

if not PW_CHARSET_PUNCTUATION_CUSTOM:
    PW_CHARSET_PUNCTUATION_CUSTOM = string.punctuation

pw_length_env = os.environ.get('PW_LENGTH', '').strip()
if pw_length_env.isdigit():
    PW_LENGTH = int(pw_length_env)
    if PW_LENGTH < 6:
        PW_LENGTH = 8
else:
    PW_LENGTH = 8

CRON_MINUTE, CRON_HOUR, CRON_DAY, CRON_MONTH, CRON_DAY_OF_WEEK = os.environ['CRONTAB_EXPRESSION'].split()

FB_ADDRESS = os.environ.get('FB_ADDRESS', '192.168.178.1')
FB_USER = os.environ['FB_USER']
FB_PASSWORD = os.environ['FB_PASSWORD']
WLAN_CONFIGURATION = os.environ.get('WLAN_CONFIGURATION', 'WLANConfiguration3')

session_max_env = os.environ.get('PW_LENGTH', '').strip()
if session_max_env.isdigit():
    WEB_APP_SESSION_MAX_LIFETIME = int(session_max_env)
else:
    WEB_APP_SESSION_MAX_LIFETIME = 30

WEB_PAGE_TITLE = os.environ.get('WEB_PAGE_TITLE', 'WLAN QR-Code')

WEB_PASSWORD = os.environ.get('WEB_PASSWORD', 'password')

WEB_PUBLIC_ENABLED = get_bool_value(os.environ.get('WEB_PUBLIC_ENABLED'), False)

WEB_WELCOME_MESSAGE_CONTENT = os.environ.get('WEB_WELCOME_MESSAGE_CONTENT', '')

GUNICORN_PORT = 5000

DEBUG = get_bool_value(os.environ.get('DEBUG'), False)