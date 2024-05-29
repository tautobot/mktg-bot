#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync;

  echo "--> Create fixture"
  python -c 'from testcases.lib.generic import * ; generate_excel_no_nricfin();';
  $SCRIPT_HOME/00.create_group_user.sh &>$WORKING_DIR_FIXTURE/fixture.log
  echo "DONE"

  echo "--> Onboard workers";
  $SCRIPT_HOME/01.onboard_worker.sh &>$WORKING_DIR_FIXTURE/onboard.log
  echo "DONE"

  echo "--> Update nricfin"
  info=$(pytest -v -s $SCRIPT_HOME/test_Essentials.py::Test::test_update_information 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/test_update_information.txt"
  fi
  printf "$result \n\n";

  echo "--> Verify can not update nricfin with existed nricfin"
  info=$(pytest -v -s $SCRIPT_HOME/test_Essentials.py::Test::test_update_information_with_existed_nricfin 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/test_update_information_with_existed_nricfin.txt"
  fi
  printf "$result \n\n";

  echo "--> Add dependent"
  dependent=$(pytest -v -s $SCRIPT_HOME/test_Essentials.py::Test::test_add_dependent 2>&1)
  result=$(echo "$dependent" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$dependent" > "$WORKING_DIR_LOGS/test_add_dependent.txt"
  fi
  printf "$result \n\n" ;

  echo "--> Verify Dependent can not add dependent"
  dependent=$(pytest -v -s $SCRIPT_HOME/test_Essentials.py::Test::test_verify_dependent_can_not_add_dependent 2>&1)
  result=$(echo "$dependent" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$dependent" > "$WORKING_DIR_LOGS/test_verify_dependent_can_not_add_dependent.txt"
  fi
  printf "$result \n\n" ;

  echo "--> Verify benefits of denpendent"
  dependent=$(pytest -v -s $SCRIPT_HOME/test_Essentials.py::Test::test_verify_benefit_of_dependent 2>&1)
  result=$(echo "$dependent" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$dependent" > "$WORKING_DIR_LOGS/test_verify_benefit_of_dependent.txt"
  fi
  printf "$result \n\n" ;

  echo "--> Verify Personal information, E-Card and Benefits of Primary on Pouch";
  benefits=$(pytest -v -s $SCRIPT_HOME/verify_Info_of_Personal_Ecard_and_Benefits.py 2>&1)
  result=$(echo "$benefits" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$benefits" > "$WORKING_DIR_LOGS/essentials_verify_Info_of_Personal_Ecard_and_Benefits.py.txt"
  fi
  printf "$result \n\n" ;

  echo "--> Verify can direct to book healthscreen page";
  visit=$(pytest -v -s $SCRIPT_HOME/verify_book_healthscreen.py 2>&1)
  result=$(echo "$visit" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$visit" > "$WORKING_DIR_LOGS/verify_book_healthscreen.txt"
  fi
  printf "$result \n\n"

#TODO fix later
#  echo "--> Verify information of Clinic"
#  info=$(pytest -v -s $SCRIPT_HOME/verify_Clinic_and_Help_page.py 2>&1)
#  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
#  if [[ "$result" == *"failed"* ]]; then
#      echo "$info" > "$WORKING_DIR_LOGS/essentials_verify_Clinic_and_Help_page.txt"
#  fi
#  printf "$result \n\n" ;
