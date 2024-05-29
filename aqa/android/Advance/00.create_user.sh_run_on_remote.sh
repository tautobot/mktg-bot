#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  #onboard workers
  $pipenv run invoke advances.onboard-create  --excel-file="/tmp/aqa/advances.xlsx"

  #create tier group
  $pipenv run invoke advances.create-tiers --excel-file="/tmp/aqa/tier_group.xlsx"