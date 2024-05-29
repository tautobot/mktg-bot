#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../../.."; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

if [[ "$environment" == 'local' ]];
  then ip=$ip_release
  else ip=$ip_docker
fi

user_at_host="trang@$ip"
SSH="ssh $user_at_host"

  echo "--> record visits"
  REMOTE_HOME=/home/autoarmour/trang; $SSH "mkdir -p $REMOTE_HOME"
  scp "$SCRIPT_HOME/02.record_visits.sh_run_on_remote.sh" $user_at_host:"$REMOTE_HOME/02.record_visits.sh_run_on_remote.sh"

  REMOTE_HOME=/home/autoarmour/trang; $SSH "mkdir -p $REMOTE_HOME"
  scp "$SCRIPT_HOME/../fixtures/visits_template.xlsx" $user_at_host:"$REMOTE_HOME/visits.xlsx"

  REMOTE_HOME=/home/autoarmour/trang; $SSH "mkdir -p $REMOTE_HOME"

  REMOTE_HOME=/home/autoarmour/trang; $SSH "mkdir -p $REMOTE_HOME"
  $SSH bash -ic "$REMOTE_HOME/02.record_visits.sh_run_on_remote.sh"
