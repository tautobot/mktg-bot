import os

# pkey of device running
pkey = f'{os.path.expanduser("~")}/.ssh/id_rsa'

# Docker
ip_docker = '34.87.182.148'

# Host
host_ip = ''
host_port = 22

# DB
db_phoenix_host = 'localhost'
db_phoenix_name = ''
db_phoenix_port = 5000
db_phoenix_user = ''
db_phoenix_pass = ''

# DIR
WORKING_DIR_LOGS    = '/tmp/aqa/aqa_logs'
WORKING_DIR_FIXTURE = '/tmp/aqa'
WORKING_DIR_REPORT  = '/tmp/aqa/automation_daily_report'

# Selenium running mode, fill 'yes' if u want to run on headless , otherwise fill 'no'
headless = ''

# Chrome driver (docker if run with container)
CHROME_DRI_ENV = "docker"

# Use to connect with release sever
user_on_host = 'trieu'
release      = f"{user_on_host}@{host_ip}"

# Env (release or local)
environment = "release"

# Device to run (android or ios)
device = 'android'

# UDID number (if run with device=ios)
UDID = ''
