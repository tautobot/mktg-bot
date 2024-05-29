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

  echo "--> Verify information on Dashboard"
  dashboard=$(pytest -v -s $SCRIPT_HOME/essentials.py 2>&1)
  result=$(echo "$dashboard" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$dashboard" > "$WORKING_DIR_LOGS/essentials_dashboard.txt"
  fi
  printf "$result \n\n"

  echo "--> Update personal information"
  info=$(pytest -v -s $SCRIPT_HOME/update_personal_information.py 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/essentials_update_personal_information.txt"
  fi
  printf "$result \n\n";

  echo "--> Add and verify benefit of dependent"
  dependent=$(pytest -v -s $SCRIPT_HOME/add_and_verify_benefit_of_dependent.py 2>&1)
  result=$(echo "$dependent" | tail -n1 | sed 's/[=]//g')
  if [[ "$result" == *"failed"* ]]; then
      echo "$dependent" > "$WORKING_DIR_LOGS/essentials_add_and_verify_benefit_of_dependent.txt"
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
