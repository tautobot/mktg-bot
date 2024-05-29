#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  #upgrade alembic
  $pipenv run alembic upgrade head

  #create group
  $pipenv run invoke group.create --name='test_aqa_loan' --uen='loan uen' --product=loan --master-policy-number=P0122348 --sponsor-message='some sponsor-message'

  #create user
  $pipenv run invoke benefits.onboard-create --excel-file="/tmp/aqa/loan.xlsx"

