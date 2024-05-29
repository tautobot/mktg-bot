#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/.."; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../"; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

if [ -d "$WORKING_DIR_LOGS" ];    then rm -Rf $WORKING_DIR_LOGS;     fi; mkdir -p $WORKING_DIR_LOGS

  pipenv install;

printf '\n\n=== FLEP ===\n\n'
  pipenv run $ROOT/aQA/src/tests/Flep/run_flep.sh

printf '\n\n=== PA ===\n\n'
  pipenv run $ROOT/aQA/src/tests/PA/run_pa.sh

printf '\n\n=== CDW ===\n\n'
  pipenv run $ROOT/aQA/src/tests/CDW/run_cdw.sh

#printf '\n\n=== PML ===\n\n'
#  pipenv run $ROOT/aQA/src/tests/PML/run_pml.sh

printf '\n\n=== Bundle ===\n\n'
  pipenv run $ROOT/aQA/src/tests/Bundle/run_bundle.sh

printf '\n\n=== Employee Benefits ===\n\n'
  pipenv run $ROOT/aQA/src/tests/EB/run_eb.sh

printf '\n\n=== MER ===\n\n'
  pipenv run $ROOT/aQA/src/tests/MER/run_mer.sh

printf '\n\n=== Health ===\n\n'
  pipenv run $ROOT/aQA/src/tests/Health/run_health.sh

printf '\n\n=== Pet ===\n\n'
  pipenv run $ROOT/aQA/src/tests/Pet/run_pet.sh

printf '\n\n=== ESSENTIALS ===\n\n'
  pipenv run $ROOT/aQA/src/tests/Essentials/run_essentials.sh

#printf '\n\n=== Zeek ===\n\n'
#  pipenv run $ROOT/aQA/src/tests/Zeek/run_zeek.sh
#
#printf '\n\n=== ExoAsia ===\n\n'
#  pipenv run $ROOT/aQA/src/tests/ExoAsia/run_exo.sh
#
