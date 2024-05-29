#!/usr/bin/env bash

#get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
s=${BASH_SOURCE} ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"

if [ "$( docker container inspect -f '{{.State.Running}}' 'mktg-chrome' )" = "true" ]; then
  echo "running...";
else
  docker-compose -f "$SCRIPT_HOME/docker-compose.yml" \
               -p 'mktg-chrome'  up \
               -d \
               --force-recreate --remove-orphans \
               --scale chrome=1
fi
