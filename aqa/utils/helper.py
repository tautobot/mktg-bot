import os
import json
import subprocess
import time
from datetime import datetime

import paramiko
import psycopg2
import requests
from sshtunnel import SSHTunnelForwarder

from aqa.utils.generic import write_to_file, generate_mobile_phl, generate_nricfin_phl
from aqa.utils.enums import url, path, account
from config_local import *


def sgt_today():
    return datetime.now().date()


def db_query_phoenix(sql, log_name=None):
    if environment == 'local':
        p_key = paramiko.RSAKey.from_private_key_file(pkey)
        with SSHTunnelForwarder(
                ssh_address_or_host=ip_release,
                ssh_pkey=p_key,
                ssh_username=user_release,
                remote_bind_address=(db_phoenix_host, db_phoenix_port)
        ) as server:
            server.start()
            params = {
                'database' : db_phoenix_name,
                'user'     : db_phoenix_user,
                'password' : db_phoenix_pass,
                'host'     : server.local_bind_host,
                'port'     : server.local_bind_port,
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(sql)
            result = curs.statusmessage
            if result not in ('SELECT 1', 'UPDATE 1') :
                result = "Can not do action on db"
            else:
                try:
                    result = curs.fetchall()[0][0]
                except:
                    pass
            conn.commit()
            conn.close()
            write_to_file(result, f'{WORKING_DIR_FIXTURE}/{log_name}.txt')
            return result

    if environment == 'release':
        output = subprocess.check_output(
            f'export  PGPASSWORD={db_phoenix_pass}; psql -h {db_phoenix_host} -U {db_phoenix_user} -d {db_phoenix_name} -p {db_phoenix_port} -c "{sql}" -o /tmp/aqa/query_result.txt',
            shell=True,
            universal_newlines=True
        )
        result = subprocess.check_output('cat /tmp/aqa/query_result.txt | tail -n3 | head -n 1', shell=True, universal_newlines=True)
        return result


def query_userId_by_email(email):
    sql = f'select id from users where email = \'{email}\''

    if environment == 'local':
        p_key = paramiko.RSAKey.from_private_key_file(pkey)
        with SSHTunnelForwarder(
                ssh_address_or_host=ip_release,
                ssh_pkey=p_key,
                ssh_username=user_release,
                remote_bind_address=(db_phoenix_host, db_phoenix_port)
        ) as server:
            server.start()
            params = {
                'database': db_phoenix_name,
                'user'    : db_phoenix_user,
                'password': db_phoenix_pass,
                'host'    : server.local_bind_host,
                'port'    : server.local_bind_port,
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(sql)
            result = curs.fetchall()
            if len(result) > 0:
                result = result[0][0]
            else:
                time.sleep(20) #wait for fixture is created
                curs.execute(sql)
                result = curs.fetchall()
            conn.close()
            return result

    if environment == 'release':
        output = subprocess.check_output(
            f'export  PGPASSWORD={db_phoenix_pass}; psql -h {db_phoenix_host} -U {db_phoenix_user} -d {db_phoenix_name} -p {db_phoenix_port} -c "{sql}" -o /tmp/aqa/user_id.txt',
            shell=True,
            universal_newlines=True
        )
        result = subprocess.check_output('cat /tmp/aqa/user_id.txt | tail -n3 | head -n 1', shell=True, universal_newlines=True)
        return result


def set_default_password(email):
    user_id = query_userId_by_email(email.lower())
    pwd = account.default_pwd_encode_bash if environment == 'release' else account.default_pwd_encode
    if user_id != [] :
        sql = f"update users set password='{pwd}' where id={user_id}"
    else:
        raise "can not found user"
    result = db_query_phoenix(sql)
    return result

def get_auth_admin():
    host = url.host_phoenix_release
    data = {
        "username" : "admin@gigacover.com",
        "password": "Test1234"
    }
    try:
        resp = requests.post(f'{host}/v2/login',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
        resp = resp.json()
        token = resp['data']['user_obj']['access_token']
        if type(token) != str:
            raise Exception('get token failed')
    except Exception as e:
        raise e

    return token

def kyc(email):
    host = url.host_phoenix_release
    data = {
        "username" : email,
        "password": "Test1234"
    }
    try:
        resp = requests.post(f'{host}/v2/login',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
        resp = resp.json()
        token = resp['data']['user_obj']['access_token']
        if type(token) != str:
            raise Exception('get token failed')
        else:
            payload = {
                "first_name": "new",
                "last_name": "name",
                "middle_name": "",
                "gender": "Female",
                "dob": "1990-01-01",
                "email": email,
                "mobile": generate_mobile_phl(),
                "id_type": "National-ID",
                "identification_no": generate_nricfin_phl(),
                "postal_code": "123456",
                "address": "new Address",
                "nature_of_self_employment": "General Worker",
                "monthly_income": "Below PHP10000",
                "source_of_funds": "Gig Worker"
            }
            resp = requests.post(f'{host}/v2/users/kyc',
                                 data=json.dumps(payload),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization' : f'Bearer {token}'})
            resp = resp.json()
            user_id = None
            if 'errors' in resp:
                if resp['errors']['debug'] == 'User already KYC':
                    user_id = 'User already KYC'
            else:
                user_id = resp['user']['id']

    except Exception as e:
        raise e

    return user_id


def create_fixture_by_sponsor(filename, filepath, template_code='INSURANCE_SCHEMA'):
    api = url.host_phoenix_release
    token = get_auth_admin()
    try:
        resp = requests.post(f'{api}/v2/sales/sponsor-file?template_code={template_code}',
                 files=[('file', (f'{filename}', open(filepath, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))],
                 headers={f'Authorization': f'Bearer {token}'})

        if template_code == 'HEALTH_SCHEMA':
            task_id = resp.json()['data']['order_created']
        else:
            task_id = resp.json()['data']["task_id"]

        if type(task_id) not in [str, int]:
            raise Exception('sponsor failed')
    except Exception as e:
       raise e

    return task_id


def build_coverage():
    cmd_to_execute = 'cd /opt/gigacover/lumber; PYTHONPATH=`pwd` /home/trang/.pyenv/shims/pipenv run python ./lumber_app/jobs/build_coverage.py -fc=SGP'

    ssh = paramiko.SSHClient()
    k = paramiko.RSAKey.from_private_key_file(f'{path.fixture_dir}/private_key')

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='35.187.235.57', username='trang', pkey=k)
    stdin, stdout, stderr = ssh.exec_command(cmd_to_execute)


def sync_user():
    cmd_to_execute = 'cd /opt/gigacover/lumber; PYTHONPATH=`pwd` /home/trang/.pyenv/shims/pipenv run python ./lumber_app/jobs/sync_user.py'

    ssh = paramiko.SSHClient()
    k = paramiko.RSAKey.from_private_key_file(f'{path.fixture_dir}/private_key')

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='35.187.235.57', username='trang', pkey=k)
    stdin, stdout, stderr = ssh.exec_command(cmd_to_execute)


def create_fixture_for_cdw(email, start_date, status, auto_renewal=True, product_name='cdw'):
    user_id = query_userId_by_email(email.lower())
    sql_phoenix = f"update order_details set start_date='{start_date}', status='{status}', coverage_created=false where user_id={user_id}"
    if auto_renewal == False:
        sql_phoenix = f"update order_details set start_date='{start_date}', status='{status}', next_prepare_date=null, next_paid_date=null, coverage_created=false  where user_id={user_id}"

    db_query_phoenix(sql_phoenix, f'{product_name}_{user_id}_{status}_{start_date}')


def get_moe_user_id(user_code):
    with open(f"{path.root_path}/config.json", "r") as jsonfile:
        data = json.load(jsonfile)

    url = f"https://api-{data['MOE_0X']}.moengage.com/v1/users/export/{data['MOE_APP_ID']}?app_id={data['MOE_APP_ID']}"

    payload = json.dumps({
        "data": {
          "identifiers": [
            {
              "identifier_type": "customer_id",
              "identifier": user_code
            }]
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic SDFYRDNHOFA5WFNPVFNENFI5RzE1RklLX0RFQlVHOkJuZDhReWVycjJ1eFpEeGRTWVdzbFhFeA==',
        'Cookie': 'AWSALB=RS6mCXGdBH8UeFBjUkyqqhNqiaKy+nsNq7hJ9utIB+7j3tKPaYZj8cDBRdoU5utHjmC2E4vjh/e0H4PQ7LQHloiTZnn/nG0HxzSeR7nhIB1QKHH2NiQZiT1OEIVp; AWSALBCORS=RS6mCXGdBH8UeFBjUkyqqhNqiaKy+nsNq7hJ9utIB+7j3tKPaYZj8cDBRdoU5utHjmC2E4vjh/e0H4PQ7LQHloiTZnn/nG0HxzSeR7nhIB1QKHH2NiQZiT1OEIVp'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    moe_user_id = response['data']['users'][0]['user_attributes']['id']
    return moe_user_id


def get_moe_event_info_by_user(moe_token, moe_user_id):
    moe_user_id= get_moe_user_id(moe_user_id)

    url = f"https://dashboard-04.moengage.com/v2/user_profile/{moe_user_id}/event_info"

    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bearer {moe_token}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    return response
