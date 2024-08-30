import os
import json
import logging
from dotenv import load_dotenv
from aqa.utils.enums import VNExNews

load_dotenv()
logger = None

config_file = None

# pkey of device running
pkey = f'{os.path.expanduser("~")}/.ssh/id_rsa'

# UDID number (if run with device=ios)
UDID        = os.environ.get('UDID')
ANDROID_DEVICE_NAME = os.environ.get('ANDROID_DEVICE_NAME')

# Accounts
LAZ_ACC  = os.environ.get('LAZ_ACC')
LAZ_PASS = os.environ.get('LAZ_PASS')

SHOPEE_ACC  = os.environ.get('SHOPEE_ACC')
SHOPEE_PASS = os.environ.get('SHOPEE_PASS')

TIKTOK_ACC    = os.environ.get('TIKTOK_ACC')
TIKTOK_PASS   = os.environ.get('TIKTOK_PASS')
TIKTOK_LOGGED = os.environ.get('TIKTOK_LOGGED')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')

SUNO_COOKIE = os.environ.get('SUNO_COOKIE')

# DIR
CODE_HOME = os.path.abspath(os.path.dirname(__file__))
PROGRESS_DIR = f"{CODE_HOME}/progress"
os.makedirs(PROGRESS_DIR, exist_ok=True)
RESOURCES_DIR = f"{CODE_HOME}/resources"
os.makedirs(RESOURCES_DIR, exist_ok=True)
ASSETS_DIR = f"{CODE_HOME}/aqa/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
LOGO_DIR = f"{ASSETS_DIR}/logo"
os.makedirs(LOGO_DIR, exist_ok=True)

# DB
db_phoenix_host = 'localhost'
db_phoenix_name = ''
db_phoenix_port = 5500
db_phoenix_user = ''
db_phoenix_pass = ''

# Selenium running mode, fill 'yes' if u want to run on headless , otherwise fill 'no'(if run on CHROME_DRI_ENV=docker skip this)
headless = 'yes'

# Chrome driver (docker/local) if docker, run chrome in docker container)
CHROME_DRI_ENV = "local"

# Docker
ip_docker = '34.87.182.148'

# Host
ip_release = '35.187.235.57'
host_port  = 22

# Use to connect with release sever
user_release = 'trieu'
release      = f"{user_release}@{ip_release}"

# Env (release or local)
environment = "release"

# Device to run (android or ios)
device = 'android'


# def load_config_file(file_path=None):
#     global config_file
#     global logger
#     global headless
#     if file_path:
#         with open(file_path) as json_data_file:
#             config_file = json.load(json_data_file)
#     logger = logging.getLogger("autobet_app")
#     logger.setLevel(logging.DEBUG)
#
#
# load_config_file(f"{CODE_HOME}/config.json")

# Google config
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


google_config = {}
def load_google_config_file():
    try:
        global google_config
        with open(f"{CODE_HOME}/{GOOGLE_APPLICATION_CREDENTIALS}") as google_json_data_file:
            google_config = json.load(google_json_data_file)
    except Exception:
        pass

def get_headless():
    try:
        return headless
    except:
        logger.error("No definition")
        return None


def set_headless(value):
    try:
        headless = value
        return headless
    except:
        logger.error("No definition)")
        return None


def set_chromedriver_env(value):
    try:
        CHROME_DRI_ENV = value
        return CHROME_DRI_ENV
    except:
        logger.error("No definition)")
        return None
