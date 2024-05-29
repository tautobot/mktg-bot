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

echo "- Run FLIP Renewals, FLEP Renewals, Sponsored Purchase";
# store result to variable and print to console
exec 5>&1
RESULT=$($ROOT/cron/scripts/automation_backend.sh | tee >(cat - >&5));
echo "[FLIP_Re/FLEP_Re/SP] Result: ";
echo -e $RESULT;
echo "END FLIP_Re/FLEP_Re/SP";

SERVICES_PATH=$ROOT/cron/services;
echo "- Send mail for automation FLIP_Re/FLEP_Re/SP...";

echo "- Collect attachments for email";
LOGS_DIR_1="/tmp/aqa_logs/flip_renewals";
LOGS_DIR_2="/tmp/aqa_logs/flep_renewals";
LOGS_DIR_3="/tmp/aqa_logs/sponsored_purchase";
ATTACHMENTS_1=""
ATTACHMENTS_2=""
ATTACHMENTS_3=""
if [ -d $LOGS_DIR_1 ]
then
    ATTACHMENTS_1=$(find $LOGS_DIR_1/* -name "*" -print0 | xargs -0 echo);
fi
if [ -d $LOGS_DIR_2 ]
then
    ATTACHMENTS_2=$(find $LOGS_DIR_2/* -name "*" -print0 | xargs -0 echo);
fi
if [ -d $LOGS_DIR_3 ]
then
    ATTACHMENTS_3=$(find $LOGS_DIR_3/* -name "*" -print0 | xargs -0 echo);
fi

ATTACHMENTS="$ATTACHMENTS_1 $ATTACHMENTS_2 $ATTACHMENTS_3";

now=$(date);
SUBJECT="Automation Test - [FLIP_Re/FLEP_Re/SP] - ($now)";
EMAIL_TO=$AQA_EMAIL_TO \
FROM_EMAIL=$AQA_FROM_EMAIL \
FROM_NAME="Automation Test Daily" \
ATTACHMENTS=$ATTACHMENTS \
$SERVICES_PATH/sendgrid.sh "$SUBJECT" "$RESULT";

echo -e "\n======= Done - Automation Test FLIP_Re/FLEP_Re/SP";