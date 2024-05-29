#!/usr/bin/env bash

WORKING_DIR="/tmp/aqa_logs/flep_renewals"
if [[ -d "$WORKING_DIR" ]]; then rm -Rf $WORKING_DIR; fi; mkdir -p -m775 $WORKING_DIR

remote_folder=$1
user=$2
host=$3

if [[ $host != "aqa-appium" ]]; then
    pipenv="/home/$user/.pyenv/shims/pipenv"
    atlas_home='/opt/gigacover/atlas'
    atlas_devops='/opt/gigacover/devops'
    source "$atlas_home/.venv/bin/activate";
else
    docker exec -it gc_atlas_tr bash;
    pipenv='/usr/local/bin/pipenv'
    atlas_home='/app'
fi

# Variables
valid_stripe_cust_id='cus_H1WDUknyyC48k4'
flepfile="$remote_folder/testfiles/flep.xlsx"
flep41file="$remote_folder/testfiles/flep41.xlsx"
flep421file="$remote_folder/testfiles/flep421.xlsx"
flep422file="$remote_folder/testfiles/flep422.xlsx"
flep81file="$remote_folder/testfiles/flep81.xlsx"
flep82file="$remote_folder/testfiles/flep82.xlsx"

# Remote Folder
flep_renewals_test_data=$remote_folder"/flep_renewals_test_data"

# Initialize summary result
summary_result='THERE IS AN ISSUE BEFORE START TESTING'

List0=(
    "CASE011"
    "CASE012"
    "CASE02"
    "CASE03"
    "CASE05"
    "CASE42"
    "CASE81"
    "CASE82"
    )
List1=(
    "CASE111"
    "CASE112"
    "CASE212"
    "CASE234"
    "CASE256"
    "CASE31"
    "CASE323"
    "CASE41"
    "CASE6123"
    )
List2=(
    "CASE523"
    )
# TODO:
List3=(
#    "CASE91"
#    "CASE92"
#    "CASE93"
    )

function append_log() {
    file="$WORKING_DIR/flep_renewals_$1.txt"
    echo "
    --------------------------
    LOG CHANGE COVERAGE ON/OFF
    --------------------------
    $2
    ----------------------
    LOG SPONSORED PURCHASE
    ----------------------
    $3
    ------------------
    LOG EMAIL REMINDER
    ------------------
    $4
    --------------------
    LOG PREPARE RENEWALS
    --------------------
    $5
    --------------------
    LOG PROCESS RENEWALS
    --------------------
    $6" >> "$file"
}

function json_value() {
    KEY=$1
    num=$2
    awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'$KEY'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${num}p
}

function create_password(){
    token=$(psql -h localhost atlas -Ujarvis -t -c "select \"resetPasswordToken\" from users where nricfin = '"$1"';" | tail -3 | head -n 1 | tr -d "[:space:]")
    create_pwd=$(curl -i -X POST "https://auth-release.gigacover.com/auth/create-password/$token"  -H 'Content-Type: application/json'  -d '{"password":"Test1234", "confirmPassword":"Test1234"}' 2>&1 | grep successfully | cut -d '>' -f22 | cut -d '<' -f1)
    if [[ $create_pwd == "Create password successfully. Please login with your password." ]]; then
        create_pwd="success"
    else
        create_pwd="failure"
    fi
}

function get_auth_token() {
    cd $atlas_home; token=`curl -X POST -H "Content-Type: application/json" -d '{"email":"'$1'","password":"'$2'"}' https://auth-release.gigacover.com/api/auth/login 2>&1 | json_value token`
}

function api_flep_change_coverage() {
    cd $atlas_home; log_change_coverage=$(curl -X POST -H "Authorization: Bearer $1" -H "Content-Type: application/json" -d '{"product": "flep", "plan": "flep80", "unit": "monthly", "coverage": "'$2'"}' https://api-release.gigacover.com/v2/settings  2>&1)
}
function invoke_sponsored_purchase() {
    if [[ $host == "release" ]]; then
        cd $atlas_home; log_sponsored_purchase=$($pipenv run invoke policy.sponsored-purchase --excel-file="$1" 2>&1)
    else
        docker exec gc_atlas_tr bash -c "mkdir -p /tmp/testfiles"
        docker cp "$remote_folder/$1" "gc_atlas_tr:/tmp/$1"
        docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke policy.sponsored-purchase --excel-file=/tmp/$1 1>/dev/null 2>&1; cd - >/dev/null"
    fi
}

# TODO: Pre-define this function to verify reminder email for losing sponsorship
function invoke_reminder_email_losing_sponsorship() {
    if [[ $host == "release" ]]; then
        cd $atlas_home; $pipenv run invoke daily.flep-reminder-email-losing-sponsorship
    else
        docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke daily.flep-reminder-email-losing-sponsorship 1>/dev/null 2>&1; cd - >/dev/null"
    fi
}

function change_coverage() {
    query="Update settings set value='"$1"' where key='coverage' and nricfin='"$2"'"
    psql -h localhost atlas -Ujarvis -t -c "$query" 1>/dev/null 2>&1; cd - >/dev/null
}

function change_unit() {
    query="Update settings set value='"$1"' where key='unit' and nricfin='"$2"'"
    psql -h localhost atlas -Ujarvis -t -c "$query" 1>/dev/null 2>&1; cd - >/dev/null
}

function change_plan() {
    query="Update settings set value='"$1"' where key='plan' and nricfin='"$2"'"
    psql -h localhost atlas -Ujarvis -t -c "$query" 1>/dev/null 2>&1; cd - >/dev/null
}

function run_flep_email_reminder() {
    cd $atlas_home; log_email_reminder=$($pipenv run invoke daily.flep-reminder-email 2>&1)
}

function run_flep_prepare_renewals() {
    cd $atlas_home; log_prepare_renewals=$($pipenv run invoke daily.flep-prepare-renewals 2>&1)
}

function run_flep_process_renewals() {
    cd $atlas_home; log_process_renewals=$($pipenv run invoke daily.flep-process-renewals 2>&1)
}

function execute_query() {
    psql -h localhost atlas -Ujarvis -t -c "$1" 1>/dev/null 2>&1; error_code=$?
}

function r_execute_query() {
    r=`psql -h localhost atlas -Ujarvis -t -c "$1" | xargs`

}

function add_invalid_card() {
    execute_query "UPDATE users SET stripe_cust_id=null WHERE nricfin='"$nricfin"';"
}

function add_valid_card() {
    execute_query "UPDATE users SET stripe_cust_id='"$valid_stripe_cust_id"' WHERE nricfin='"$nricfin"';"
}

function setup_existing_policy_and_settings() {
    s1="UPDATE policies SET status='"$status"', policy_start='"$policy_start"', policy_end='"$policy_end"' WHERE nricfin='"$nricfin"' AND policy_number like '%-001';"
    s2="UPDATE settings SET value='"$coverage"' WHERE key='coverage' and nricfin='"$nricfin"';"
    s3="UPDATE settings SET value='"$plan"' WHERE key='plan' and nricfin='"$nricfin"';"
    s4="UPDATE settings SET value='"$unit"' WHERE key='unit' and nricfin='"$nricfin"';"
    execute_query "$s1"
    execute_query "$s2"
    execute_query "$s3"
    execute_query "$s4"
}

summary_result='PASS'

printf "%-15s  %-10s\n" "TEST CASE NO." "RESULT";
invoke_sponsored_purchase $flepfile

while read line; do
    # Reading each line
    CASE_ID=$(echo $line | cut -d':' -f 1)

    case_data=($(echo $line | tr ":" "\n"))
    data=($(echo ${case_data[1]} | tr "," "\n"))

    nricfin=${data[0]}
    email=${data[1]}
    policy_start=${data[2]}
    policy_end=${data[3]}
    status=${data[4]}
    plan=${data[5]}
    unit=${data[6]}
    coverage=${data[7]}

    g_policy=${data[8]}
    g_policy_start=${data[9]}
    g_policy_end=${data[10]}
    g_status=${data[11]}
    g_plan=${data[12]}
    g_unit=${data[13]}

    # NON-CONTINUOUS CASES NEED MORE VARIABLES
    if [[ $CASE_ID == "CASE72" ]]; then
        second_policy_start=${data[14]}
        second_policy_end=${data[15]}
        changed_first_policy_start=${data[16]}
        changed_first_policy_end=${data[17]}
        changed_second_policy_start=${data[18]}
        changed_second_policy_end=${data[19]}
    elif [[ $CASE_ID == "CASE81" ]]; then
        changed_policy_start=${data[14]}
        changed_policy_end=${data[15]}
    fi

    for entry in "${List0[@]}"
    do
        if [[ "$entry" == "$CASE_ID" ]]; then
            if [[ "$entry" == "CASE011" ]]; then
                setup_existing_policy_and_settings
            elif [[ "$entry" == "CASE42" ]]; then
                invoke_sponsored_purchase $flep421file
            elif [[ "$entry" == "CASE81" ]]; then
                invoke_sponsored_purchase $flep81file
            elif [[ "$entry" == "CASE82" ]]; then
                invoke_sponsored_purchase $flep82file
            fi
            run_flep_email_reminder
            q="SELECT value FROM settings
                WHERE key = 'coverage' AND nricfin = '"$nricfin"';"
            r_execute_query "$q"
            if [[ "$entry" == "CASE05" ]]; then
                passfail=`if [[ "$r" == "off" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
            elif [[ "$entry" == "CASE42" || "$entry" == "CASE81" || "$entry" == "CASE82" ]]; then
                if [[ "$r" == "off" ]]; then
                    if [[ "$entry" == "CASE81" ]]; then
                        u="UPDATE policies SET status='expired', policy_start='"$changed_policy_start"', policy_end='"$changed_policy_end"' WHERE nricfin='"$nricfin"' AND policy_number like '%-001';"
                        execute_query "$u"
                    fi
                    add_valid_card
                    get_auth_token $email $nricfin  # nricfin = pass by default
                    api_flep_change_coverage $token "on"
                    q1="SELECT COUNT(*) FROM policies
                        WHERE status = 'paid' AND nricfin = '"$nricfin"';"
                    r_execute_query "$q1"
                    r1=$r
                    if [[ "$r1" == "1" ]]; then
                        if [[ "$entry" == "CASE42" ]]; then
                            invoke_sponsored_purchase $flep422file
                            q1="SELECT COUNT(*) FROM policies
                                WHERE nricfin = '"$nricfin"' AND status = '"$g_status"' AND policy_start = '"$g_policy_start"' AND policy_end = '"$g_policy_end"';"
                            q2="SELECT COUNT(*) FROM policies
                                WHERE status = 'cancelled' AND nricfin = '"$nricfin"';"
                            r_execute_query "$q1"
                            r1=$r
                            r_execute_query "$q2"
                            r2=$r
                            passfail=`if [[ "$r1" == "1" && "$r2" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                        else
                            q1="SELECT EXISTS (SELECT 1 FROM policies
                                WHERE nricfin = '"$nricfin"' AND status = '"$g_status"' AND policy_start = '"$g_policy_start"' AND policy_end = '"$g_policy_end"');"
                            r_execute_query "$q1"
                            r1=$r
                            passfail=`if [[ "$r1" == "$g_policy" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                        fi
                    else
                        passfail="FAIL"
                        printf "%-15s  %-10s\n" $CASE_ID $passfail
                    fi
                else
                    passfail="FAIL"
                    printf "%-15s  %-10s\n" $CASE_ID $passfail
                fi
            elif [[ "$entry" == "CASE011" ]]; then
                passfail=`if [[ "$r" == "on" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
            else
                passfail=`if [[ "$r" == "off" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
            fi
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL";
                append_log "$CASE_ID" "$log_change_coverage" "$log_sponsored_purchase" "$log_email_reminder" "$log_prepare_renewals" "$log_process_renewals"
            fi
    fi
    done

    for entry in "${List1[@]}"
    do
        if [[ "$entry" == "$CASE_ID" ]]; then
            setup_existing_policy_and_settings
            if [[ "$entry" != "CASE31" && "$entry" != "CASE323" ]]; then
                run_flep_prepare_renewals
            fi
            if [[ "$entry" != "CASE112" && "$entry" != "CASE41" && "$entry" != "CASE6123" ]]; then
                run_flep_process_renewals
            fi
            q1="SELECT COUNT(*) FROM policies
                WHERE status = 'prepared' AND nricfin = '"$nricfin"';"
            q2="SELECT COUNT(*) FROM policies
                WHERE status = 'paid' AND nricfin = '"$nricfin"';"
            r_execute_query "$q1"
            r1=$r
            r_execute_query "$q2"
            r2=$r

            if [[ "$entry" == "CASE212" ]]; then
                passfail=`if [[ "$r1" == "0" && "$r2" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
            elif [[ "$entry" == "CASE112" ]]; then
                if [[ "$r1" == "1" && "$r2" == "0" ]]; then
                    add_invalid_card
                    run_flep_process_renewals
                    r_execute_query "$q2"
                    r2=$r
                    passfail=`if [[ "$r2" == "0" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                else
                    passfail="FAIL"
                    printf "%-15s  %-10s\n" $CASE_ID $passfail
                fi
            elif [[ "$entry" == "CASE31" || "$entry" == "CASE323" ]]; then
                add_valid_card
                if [[ "$entry" == "CASE323" ]]; then
                    run_flep_prepare_renewals
                fi

                run_flep_process_renewals
                q3="SELECT COUNT(*) FROM policies
                WHERE status = 'paid' AND nricfin = '"$nricfin"' AND sponsor='gigacover';"
                r_execute_query "$q3"
                r3=$r
                if [[ "$entry" == "CASE31" ]]; then
                    passfail=`if [[ "$r3" == "0" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                else
                    passfail=`if [[ "$r3" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                fi
            elif [[ "$entry" == "CASE41" ]]; then
                if [[ "$r1" == "1" ]]; then
                    invoke_sponsored_purchase $flep41file
                    q1="SELECT COUNT(*) FROM policies
                        WHERE status = 'prepared' AND nricfin = '"$nricfin"';"
                    q2="SELECT COUNT(*) FROM policies
                        WHERE nricfin = '"$nricfin"' AND status = '"$g_status"' AND policy_start = '"$g_policy_start"' AND policy_end = '"$g_policy_end"';"
                    r_execute_query "$q1"
                    r1=$r
                    r_execute_query "$q2"
                    r2=$r
                    passfail=`if [[ "$r1" == "0" && "$r2" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                else
                    passfail="FAIL"
                    printf "%-15s  %-10s\n" $CASE_ID $passfail
                fi
            elif [[ "$entry" == "CASE6123" ]]; then
                if [[ "$r1" == "1" ]]; then
                    create_password $nricfin
                    get_auth_token $email "Test1234"
                    api_flep_change_coverage $token "off"
                    #change_coverage "off" $nricfin
                    run_flep_process_renewals
                    r_execute_query "$q1"
                    r1=$r
                    r_execute_query "$q2"
                    r2=$r
                    if [[ "$r1" == "0" && "$r2" == "0" ]]; then
                        api_flep_change_coverage $token "on"
                        #change_coverage "on" $nricfin
                        run_flep_prepare_renewals
                        add_invalid_card
                        run_flep_process_renewals
                        r_execute_query "$q1"
                        r1=$r
                        r_execute_query "$q2"
                        r2=$r
                        if [[ "$r1" == "1" && "$r2" == "0" ]]; then
                            add_valid_card
                            run_flep_process_renewals
                            r_execute_query "$q1"
                            r1=$r
                            r_execute_query "$q2"
                            r2=$r
                            passfail=`if [[ "$r1" == "0" && "$r2" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                        else
                            passfail="FAIL"
                            printf "%-15s  %-10s\n" $CASE_ID $passfail
                        fi
                    else
                        passfail="FAIL"
                        printf "%-15s  %-10s\n" $CASE_ID $passfail
                    fi
                else
                    passfail="FAIL"
                    printf "%-15s  %-10s\n" $CASE_ID $passfail
                fi
            else
                passfail=`if [[ "$r1" == "0" && "$r2" == "0" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
            fi
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL";
                append_log "$CASE_ID" "$log_change_coverage" "$log_sponsored_purchase" "$log_email_reminder" "$log_prepare_renewals" "$log_process_renewals"
            fi
    fi
    done

    for entry in "${List2[@]}"
    do
        if [[ "$entry" == "$CASE_ID" ]]; then
            setup_existing_policy_and_settings
            run_flep_prepare_renewals

            q1="SELECT EXISTS (SELECT 1 FROM policies
                WHERE nricfin = '"$nricfin"' AND status = '"$g_status"' AND policy_start = '"$g_policy_start"' AND policy_end = '"$g_policy_end"');"

            r_execute_query "$q1"
            if [[ "$r" == "$g_policy" ]]; then
                if [[ "$entry" == "CASE523" ]]; then
                    run_flep_prepare_renewals
                    q1="SELECT COUNT(*) FROM policies
                        WHERE status = '"$g_status"' AND nricfin = '"$nricfin"';"
                    r_execute_query "$q1"
                    passfail=`if [[ "$r" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; printf "%-15s  %-10s\n" $CASE_ID $passfail
                    if [[ "$passfail" == "FAIL" ]]; then append_log "$CASE_ID"; fi
                else
                    printf "%-15s  %-10s\n" $CASE_ID "PASS";
                fi
            else
                printf "%-15s  %-10s\n" $CASE_ID "FAIL";
                append_log "$CASE_ID" "$log_change_coverage" "$log_sponsored_purchase" "$log_email_reminder" "$log_prepare_renewals" "$log_process_renewals"
            fi
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL";
            fi
        fi
    done

done < $flep_renewals_test_data


# SUMMARY
if [[ "$summary_result" == "FAIL" ]]; then
echo '

FLEP RENEWALS: FAIL'
elif [[ "$summary_result" == "PASS" ]]; then
echo '

FLEP RENEWALS: PASS'
else
echo "

FLEP RENEWALS: $summary_result"
fi