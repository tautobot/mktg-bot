#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../.."; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../"; ROOT=$(cd "$ROOT" && pwd)


source "$ROOT/config_local.py";

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync; mkdir "/tmp/aqa/aqa_logs"


  echo '--> Buy CDW on venta'
  export PYTEST_CURRENT_TEST=test_self_bought_cdw
  pytest -n 2 $SCRIPT_HOME/test_self_bought_cdw.py


  echo '--> Run test for CDW on Web Portal'
  export PYTEST_CURRENT_TEST=test_cdw_web_portal
  pytest $SCRIPT_HOME/test_cdw_web_portal.py
