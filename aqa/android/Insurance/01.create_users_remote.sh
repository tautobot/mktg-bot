#!/usr/bin/env bash
pipenv=$1

cd /opt/gigacover/atlas >/dev/null 2>&1

  $pipenv run invoke policy.sponsored-purchase --excel-file="/tmp/aqa/flep.xlsx"
