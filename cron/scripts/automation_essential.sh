#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s";
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);

echo "ROOT PATH: $ROOT";

# Get env variables (AQA_EMAIL_TO, AQA_FROM_EMAIL)
source $ROOT/cron/scripts/.env

echo "- Export PYTHONPATH";
export PYTHONPATH=$PYTHONPATH:$ROOT;

echo "- Setup pyenv Path (to run pipenv in ~/.pyenv/shims)";
export PATH="~/.pyenv/shims:$PATH";

echo "- Active virtual environment...";
cd $ROOT; pipenv sync;
source $ROOT/.venv/bin/activate;

echo "- Run run_Essentials.sh";
# store result to variable and print to console
exec 5>&1
RESULT=$($ROOT/aQA/android/src/Essentials/run_essentials.sh | tee >(cat - >&5));
echo "[Essentials] Result: ";
echo -e $RESULT;
echo "END run_Essentials.sh";

SERVICES_PATH=$ROOT/cron/services;
echo "- Send mail for automation test Essentials ...";

echo "- Collect attachments for email";
LOGS_DIR="/tmp/aqa_logs/essentials";
ATTACHMENTS=""
if [ -d $LOGS_DIR ]
then
    ATTACHMENTS=$(find $LOGS_DIR/* -name "*" -print0 | xargs -0 echo);
fi

#echo $ATTACHMENTS;

now=$(date);
SUBJECT="Automation Test - [Essentials] - ($now)";
EMAIL_TO=$AQA_EMAIL_TO \
FROM_EMAIL=$AQA_FROM_EMAIL \
FROM_NAME="Automation Test Daily" \
ATTACHMENTS=$ATTACHMENTS \
$SERVICES_PATH/sendgrid.sh "$SUBJECT" "$RESULT";

echo -e "\n======= Done - Automation Test Essentials";