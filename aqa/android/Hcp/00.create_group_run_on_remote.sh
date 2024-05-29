#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  #upgrade alembic
  $pipenv run alembic upgrade head

  #run db.seed-product-template
  $pipenv run invoke db.seed-product-template

  #add variable
  $pipenv run invoke template.create-variable-w-excel --excel-file='/tmp/aqa/variable.xlsx'

  #apply product template
  $pipenv run invoke template.create-w-excel --excel-file='/tmp/aqa/template.xlsx'

  #create group
  $pipenv run invoke group.create --name=test_aqa_hcp --uen='test_aqa_hcp uen' --product=advances --master-policy-number=AV12233366 --sponsor-message='some sponsor-message'
