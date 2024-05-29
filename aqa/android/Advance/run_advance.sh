#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";


cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync;

  echo "--> Onboard advance"
  $SCRIPT_HOME/00.create_group_user.sh &>$WORKING_DIR_FIXTURE/fixture_advance.log
  echo "DONE"

  echo "--> Verify display correct and request success"
  info=$(pytest -v -s $SCRIPT_HOME/test_advance.py 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/advance.txt"
  fi
  printf "$result \n";
