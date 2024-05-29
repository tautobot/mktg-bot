import os
from datetime import datetime
from os import environ
import json
import uuid
import base64
import http.client
from aqa.utils.generic import read_file
from config_local import WORKING_DIR_LOGS
from dotenv import load_dotenv

load_dotenv()

CONTENT = read_file(f"{WORKING_DIR_LOGS}/aqa_daily.txt")

email_tos = environ.get("AQA_EMAIL_TO")
list_email_to = {}
if email_tos:
  list_email_to = email_tos.split(',')
  list_email_to = [{"email": item} for item in list_email_to if item]

list_att = []
attachments = os.listdir(WORKING_DIR_LOGS)
if attachments:
  for att_path in attachments:
    name = att_path.split('/')[-1]
    data = open(f'{WORKING_DIR_LOGS}/{att_path}', "rb").read()
    b64_encoded = base64.b64encode(data)
    item = {
      "content": b64_encoded.decode('utf-8'),
      "type": "txt",
      "name": name,
      "filename": name,
      "disposition": "inline",
      "content_id": uuid.uuid1().__str__()
    }
    list_att.append(item)

body_dict = {
  "personalizations": [
    {"to": list_email_to}
  ],
  "from": {
    "email": environ.get('AQA_FROM_EMAIL'),
  },
  "subject": f'Automation Test - ({datetime.now().strftime("%A %d %b %Y %X")})',
  "content": [{"type": "text/plain", "value": CONTENT}],
}

if list_att:
  body_dict['attachments'] = list_att


conn = http.client.HTTPSConnection('api.sendgrid.com')
sendgrid_key = environ.get('SENDGRID_API_KEY')
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % sendgrid_key}
json_data = json.dumps(body_dict)
conn.request('POST', '/v3/mail/send', json_data, headers)
response = conn.getresponse()
print(response.read().decode())

