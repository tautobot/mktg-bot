#!/usr/bin/env bash

pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  #upgrade alembic
  $pipenv run alembic upgrade head

  #create group
  $pipenv run invoke group.create --name='test_aqa_insurance' --uen='some uen 1' --product=flep --master-policy-number=P0122347 --sponsor-message='some sponsor-message'
