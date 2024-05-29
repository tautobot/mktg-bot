#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  #sponsor user
  $pipenv run invoke policy.sponsored-purchase --excel-file="/tmp/aqa/hcp.xlsx"
  $pipenv run invoke user.onboard --excel-file="/tmp/aqa/hcp_nonric_template.xlsx"
