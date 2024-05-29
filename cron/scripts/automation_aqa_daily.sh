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

echo "- Run aqa_daily.sh";
# store result to variable and print to console
exec 5>&1

RESULT=$($ROOT/cron/daily_cronjob_aqa/aqa_daily.sh | tee >(cat - >&5));
echo "[Automation Test] Result: ";
echo -e $RESULT;
echo "END aqa_daily.sh";

#SERVICES_PATH=$ROOT/cron/services;
#echo "- Send mail for automation test ...";
#
#echo "- Collect attachments for email";
#LOGS_DIR_1="/tmp/aqa/aqa_logs";
#ATTACHMENTS_1=""
#if [ -d $LOGS_DIR_1 ]
#then
#    ATTACHMENTS_1=$(find $LOGS_DIR_1/* -name "*" -print0 | xargs -0 echo);
#fi
#
#ATTACHMENTS="$ATTACHMENTS_1";
#
##echo $ATTACHMENTS;
#
#now=$(date);
#SUBJECT="Automation Test - ($now)";
#EMAIL_TO=$AQA_EMAIL_TO \
#FROM_EMAIL=$AQA_FROM_EMAIL \
#FROM_NAME="Automation Test Daily" \
#ATTACHMENTS=$ATTACHMENTS \
#$SERVICES_PATH/sendgrid.sh "$SUBJECT" "$RESULT";
#
#echo -e "\n======= Done - Automation Test";
