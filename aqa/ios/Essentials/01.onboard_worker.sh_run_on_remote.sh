#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  $pipenv run invoke benefits.onboard-create --excel-file="/tmp/aqa/benefits.xlsx"
