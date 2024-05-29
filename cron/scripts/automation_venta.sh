#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s";
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);

echo "ROOT PATH: $ROOT";
echo "- Copy config.example.py to config.py";
CONFIG_PATH=$ROOT/config.py;
rm $CONFIG_PATH || true;
cp $ROOT/config_example.py $CONFIG_PATH;

#echo "2. Add some variables into config.py";
#===START Append setting to config.py
cat >> $CONFIG_PATH <<EOL

#ssh on host: aqa will be run on host which is found (available and valuable) and order by docker -> release -> staging
# docker="jarvis@34.87.120.231"
#release="autoarmour@35.187.235.57"
#staging="autoarmour@35.247.189.231"
EOL
#===END

echo "- Export PYTHONPATH";
export PYTHONPATH=$PYTHONPATH:$ROOT;

echo "- Setup pyenv Path (to run pipenv in ~/.pyenv/shims)";
export PATH="~/.pyenv/shims:$PATH";

echo "- Active virtual environment...";
cd $ROOT; pipenv sync;
source $ROOT/.venv/bin/activate;

echo "- Stop & Start Docker"
$ROOT/testcases/aQA/android/docker/stop.sh
$ROOT/testcases/aQA/android/docker/compose-up.sh

echo "- Run venta_docker.sh";
# store result to variable and print to console
exec 5>&1
RESULT=$($ROOT/testcases/aQA/aQA_venta/src/scenario/aQA/venta_docker.sh | tee >(cat - >&5));
echo "[VENTA] Result: ";
echo -e $RESULT;
echo "END venta_docker.sh";

SERVICES_PATH=$ROOT/cron/services;
echo "- Send mail for automation test VENTA...";

now=$(date);
SUBJECT="Automation Test - [VENTA] - ($now)";
EMAIL_TO="duc.le@gigacover.com,trang.truong@gigacover.com" \
FROM_EMAIL="developers@gigacover.com" \
FROM_NAME="Automation Test Daily" $SERVICES_PATH/sendgrid.sh "$SUBJECT" "$RESULT";
echo -e "\n======= Done - Automation Test VENTA";