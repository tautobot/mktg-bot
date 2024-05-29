#!/usr/bin/env bash
force_pipenv_sync=$1

cd /opt/autoarmour/atlas

  REMOTE_HOME=/home/autoarmour/trang;
  pipenv run invoke benefits.record-visit  --file="$REMOTE_HOME/visits.xlsx"