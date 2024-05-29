#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s";
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);

echo "ROOT PATH: $ROOT";

# Get env variables (AQA_EMAIL_TO, AQA_FROM_EMAIL)
source $ROOT/cron/scripts/.env
#echo $AQA_EMAIL_TO;
#echo $AQA_FROM_EMAIL;

echo "- Run Automation Test Sample Job...";
# store result to variable and print to console
exec 5>&1
RESULT=$($ROOT/cron/scripts/sample_job.sh | tee >(cat - >&5));

echo "Result: ";
echo -e $RESULT;

SERVICES_PATH=$ROOT/cron/services;
echo "- Send mail for Automation Test Sample Job...";

now=$(date);
SUBJECT="Automation Test - [Sample Job] - ($now)";
EMAIL_TO=$AQA_EMAIL_TO \
FROM_EMAIL=$AQA_FROM_EMAIL \
FROM_NAME="Automation Test Daily" $SERVICES_PATH/sendgrid.sh "$SUBJECT" "$RESULT";

echo -e "\n======= Done - Automation Test Sample Job";