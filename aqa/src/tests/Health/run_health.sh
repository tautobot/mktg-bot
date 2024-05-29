#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../.."; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../"; ROOT=$(cd "$ROOT" && pwd)


source "$ROOT/config_local.py";

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync; mkdir "/tmp/aqa/aqa_logs"


echo "--> Create fixture"
cat << EOF > $WORKING_DIR_FIXTURE/temp_script.py  #create python file to create fixture
from aQA.utils.helper import create_fixture_by_sponsor
from aQA.utils.enums import path
from aQA.utils.generic import cook_fixture_health

file_name  = 'health_template.xlsx'
file_path = f'{path.fixture_dir}/{file_name}'

cook_fixture_health(file_name)
task_id = create_fixture_by_sponsor(file_name, file_path, 'HEALTH_SCHEMA')
print(f"order_created:  {task_id}")
EOF

python $WORKING_DIR_FIXTURE/temp_script.py &>$WORKING_DIR_FIXTURE/create_fixture_health.log
rm -rf $WORKING_DIR_FIXTURE/temp_script.py 2>&1   #remove file after create fixture is done
printf "DONE \n\n"


  echo '--> Run testcase for Health on venta'
  export PYTEST_CURRENT_TEST=test_health_venta
  pytest $SCRIPT_HOME/test_health_venta.py


  echo "--> Run test for Health on Web Portal"
  export PYTEST_CURRENT_TEST=test_health_on_web_portal
  pytest $SCRIPT_HOME/test_health_web_portal.py
