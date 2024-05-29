#!/usr/bin/env bash
pipenv=$1
email='test_aQA_benefits@gigacover.com'

cd /opt/gigacover/atlas >/dev/null 2>&1

  #upgrade alembic
  $pipenv run alembic upgrade head

  #create group
  $pipenv run invoke group.create --name='test_aqa_benefits' --uen='some uen' --product=benefits --master-policy-number=P0122346 --sponsor-message='some sponsor-message'

  #create user
  $pipenv run invoke user.create $email Test1234 User --role=owner --group='test_aqa_benefits' --nricfin=AE1123125 --system='group' --country='SGP' 2>/tmp/aqa/user2.log