#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../.."; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync; mkdir "/tmp/aqa/aqa_logs"


  echo "--> Run test for MER on Dashboard"
  export PYTEST_CURRENT_TEST=test_mer_on_dashboard
  pytest $SCRIPT_HOME/test_mer_on_dashboard.py
