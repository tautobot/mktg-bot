#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1
email='test_advances@gigacover.com'
email_tier='test_advances_tier@gigacover.com'

  #upgrade alembic
  $pipenv run alembic upgrade head

  #create group
  $pipenv run invoke group.create --name=test_aqa_advances --uen='test_aqa_advances uen' --product=advance --master-policy-number=AV12233345 --sponsor-message='some sponsor-message'
  $pipenv run invoke group.create --name=test_aqa_advances_tier --uen='test_aqa_advances_tier uen' --product=advance --master-policy-number=AV12233346 --sponsor-message='some sponsor-message'

  #create user
  $pipenv run invoke user.create $email Test1234 User --role=owner --group='test_aqa_advances' --nricfin=AE1123129 --system='group' --country='IDN' 2>/tmp/aqa/owner_advance.log
  $pipenv run invoke user.create $email_tier Test1234 User --role=owner --group='test_aqa_advances_tier' --nricfin=AE1123130 --system='group' --country='IDN' 2>/tmp/aqa/owner_advance_tier.log

