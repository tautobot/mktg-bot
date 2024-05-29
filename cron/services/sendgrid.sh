#!/bin/bash

DOCSTRING=cat << EOF
    EMAIL_TO is list email, separate by ","
    ./sendgrid.sh {email_subject} {email_content}

    Sample Use:
      ATTACHMENTS="" ./cron/services/sendgrid.sh "Test subject mail" "test content"
EOF

# Set variables
SENDGRID_API_KEY="";

### variables from tmp env
if [[ -z "$EMAIL_TO" ]]; then EMAIL_TO="duc.le@gigacover.com"; fi
if [[ -z "$FROM_EMAIL" ]]; then FROM_EMAIL="hey@gigacover.com"; fi
if [[ -z "$FROM_NAME" ]]; then FROM_NAME='Hey Gigacover'; fi
if [[ -z "$ATTACHMENTS" ]]; then ATTACHMENTS=''; fi

### Variables from args
EMAIL_SUBJECT=$1;
if [[ -z "$EMAIL_SUBJECT" ]]; then
  echo "Please input email subject";
  exit 1
fi

EMAIL_CONTENT=$2
if [[ -z "$EMAIL_CONTENT" ]]; then
  echo "Please input email content";
  exit 1
fi

echo "SUBJECT: $EMAIL_SUBJECT";

function build_body {
  FROM_EMAIL=$FROM_EMAIL FROM_NAME=$FROM_NAME \
  EMAIL_TO=$EMAIL_TO EMAIL_SUBJECT=$EMAIL_SUBJECT \
  EMAIL_CONTENT=$EMAIL_CONTENT \
  SENDGRID_API_KEY=$SENDGRID_API_KEY \
  python - <<END
from os import environ
import json
import uuid
import base64
import http.client

email_tos = environ.get('EMAIL_TO')
if email_tos:
  list_email_to = email_tos.split(',')
  list_email_to = [{"email": item} for item in list_email_to if item]

attrs = environ.get('ATTACHMENTS', '').strip()
list_att = []
if attrs:
  for att_path in attrs.split(' '):
    name = att_path.split('/')[-1]
    data = open(att_path, "rb").read()
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
    "email": environ.get('FROM_EMAIL'),
    "name": environ.get('FROM_NAME')
  },
  "subject": environ.get('EMAIL_SUBJECT'),
  "content": [{"type": "text/plain", "value": environ.get('EMAIL_CONTENT')}],
}

if list_att:
  body_dict['attachments'] = list_att

#print(json.dumps(body_dict))

conn = http.client.HTTPSConnection('api.sendgrid.com')
sendgrid_key = environ.get('SENDGRID_API_KEY')
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % sendgrid_key}
json_data = json.dumps(body_dict)
conn.request('POST', '/v3/mail/send', json_data, headers)
response = conn.getresponse()
print(response.read().decode())
END
}

TEXT=$(build_body)
echo "EMAIL CONTENT: $TEXT";

curl --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --header 'Authorization: Bearer '$SENDGRID_API_KEY \
  --header 'Content-Type: application/json' \
  --data "'$TEXT'"