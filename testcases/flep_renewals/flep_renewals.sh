#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);
green=$(tput setaf 2)
red=$(tput setaf 1)
normal=$(tput sgr0)
yellow=$(tput setaf 3)


# cd $ROOT; ./testcases/aQA/android/docker/stop.sh
cd $ROOT; ./testcases/venta/aQA_venta/docker/compose-up.sh
cd $ROOT; export PYTHONPATH=$PYTHONPATH:$ROOT ;pipenv sync
source $ROOT/.venv/bin/activate
CONFIG="$SCRIPT_HOME/config.py"
source $CONFIG
feature="flep_renewals"
user=$USER
host=$HOSTNAME
userhost="$user@$host"

ListTCs=(
    "CASE011"
    "CASE012"
    "CASE02"
    "CASE03"
    "CASE05"
    "CASE111"
    "CASE112"
    "CASE212"
    "CASE234"
    "CASE256"
    "CASE31"
    "CASE323"
    "CASE41"
    "CASE42"
    "CASE523"
    "CASE6123"
    "CASE81"
    "CASE82"
    )

printf 'Generating data for FLEP Auto Renewals... '
printf "" | tee $SCRIPT_HOME/flep_renewals_test_data
printf "" | tee /tmp/aQA/nricfin
printf "" | tee /tmp/aQA/email

for caseId in "${ListTCs[@]}"
do
    #((start_venta=start_venta+1))
    if [[ $caseId == "CASE011" || $caseId == "CASE111" || $caseId == "CASE111" || $caseId == "CASE212" || \
          $caseId == "CASE234" || $caseId == "CASE256" || $caseId == "CASE41" || $caseId == "CASE523" || \
          $caseId == "CASE6123" || $caseId == "CASE72" ]]; then
        python $ROOT/testcases/venta/aQA_venta/src/scenario/venta/venta_flep.py "range1" "$dri" "$environment" 1>/dev/null 2>&1; cd - >/dev/null
    fi
    python $SCRIPT_HOME/flep_renewals_data_generator.py $caseId
done
echo 'DONE'

if [[ $userhost != "trieu@release" && $userhost != "jarvis@release" && $userhost != "jarvis@aqa-appium" ]]; then
    if [[ -z $docker ]]; then
        if [[ -z $release ]]; then
            echo "Cannot find out any host in config file. AQA Sponsored Purchase will exit in";
            countdown "00:00:03";
            exit
        else remote_host=$release; echo "${green}AQA FLEP AUTO RENEWALS on release - $remote_host${normal}"; fi
    else remote_host=$docker; echo "${green}AQA FLEP AUTO RENEWALS on docker - $remote_host${normal}"; fi

    ssh_host=$(echo $remote_host | cut -d'@' -f 2);
    remote_folder="/opt/gigacover/aqa/$feature/$userhost";

    printf "Copying testing files to server... "
    # Copy script to :remote_host
    ssh "$remote_host" "mkdir -p $remote_folder"
    ssh "$remote_host" "mkdir -p $remote_folder/testfiles"
    scp "$SCRIPT_HOME/flep_renewals_verify.sh" "$remote_host:$remote_folder/flep_renewals_verify.sh" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep.xlsx" "$remote_host:$remote_folder/testfiles/flep.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep41.xlsx" "$remote_host:$remote_folder/testfiles/flep41.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep421.xlsx" "$remote_host:$remote_folder/testfiles/flep421.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep422.xlsx" "$remote_host:$remote_folder/testfiles/flep422.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep81.xlsx" "$remote_host:$remote_folder/testfiles/flep81.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/testfiles/flep82.xlsx" "$remote_host:$remote_folder/testfiles/flep82.xlsx" 1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/flep_renewals_test_data" "$remote_host:$remote_folder/flep_renewals_test_data" 1>/dev/null 2>&1; cd - >/dev/null
    echo "DONE"

    echo 'Executing FLEP Auto Renewals...'
    ssh "$remote_host" "$remote_folder/flep_renewals_verify.sh $remote_folder $user $host"
else
    "$SCRIPT_HOME/flep_renewals_verify.sh" $SCRIPT_HOME $user $host
fi


