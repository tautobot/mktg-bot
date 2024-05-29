#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync;

  echo "--> Sponsored purchase HCP"
  $SCRIPT_HOME/00.create_group_user.sh &> $WORKING_DIR_FIXTURE/fixture_hcp.log
  echo "DONE"

  echo "--> Verify Claim success with Eng language"
  info=$(pytest -v -s $SCRIPT_HOME/test_hcp.py::Test::test_claim_Eng_UI 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/Claim_hcp_Eng_UI.txt"
  fi
  printf "$result \n";

  echo "--> Verify Claim success with Bahasa language"
  info=$(pytest -v -s $SCRIPT_HOME/test_hcp.py::Test::test_claim_Indo_UI 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/Claim_hcp_Indo_UI.txt"
  fi
  printf "$result \n";

  echo "--> Self Bought HCP on Pouch"
  info=$(pytest -v -s $SCRIPT_HOME/test_hcp.py::Test::test_self_bought_hcp 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/self_bought_hcp.txt"
  fi
  printf "$result \n";
