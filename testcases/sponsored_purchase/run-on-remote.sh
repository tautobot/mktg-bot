#!/usr/bin/env bash

WORKING_DIR='/tmp/aqa_logs/sponsored_purchase'
if [[ -d "$WORKING_DIR" ]]; then rm -Rf $WORKING_DIR; fi; mkdir -p -m775 $WORKING_DIR

remote_folder=$1
user=$2
host=$3

if [[ $host == "release" ]]; then
    pipenv="/home/$user/.pyenv/shims/pipenv"
    atlas_home='/opt/gigacover/atlas'
    source "$atlas_home/.venv/bin/activate";
else
    docker exec -it gc_atlas_tr bash;
    pipenv='/usr/local/bin/pipenv'
    atlas_home='/app'
fi

function append_log() {
    file="$WORKING_DIR/sponsored_purchase_$1.txt"
    echo "`date`
    ----------------------
    LOG SPONSORED PURCHASE
    ----------------------
    $2" | tee > "$file"
}

function pipenv_run_invoke_create_group_host() {
    query_master_policy_number_flep="SELECT count(*) FROM master_policy_numbers where sponsor = 'gojek goalbetter' and product = 'flep';"
    query_master_policy_number_flip="SELECT count(*) FROM master_policy_numbers where sponsor = 'gojek goalbetter' and product = 'flip';"
    query_master_policy_number_pa="SELECT count(*) FROM master_policy_numbers where sponsor = 'gis' and product = 'pa';"
    query_master_policy_number_pa="SELECT count(*) FROM master_policy_numbers where sponsor = 'gis' and product = 'gpac';"
    printf "CREATE MASTER POLICY NUMBER FOR FLIP, FLEP, PA, GPAC"
    if [[ $host == "release" ]]; then
        psql_atlas_postgres_host "$query_master_policy_number_flep"
        if [[ "$result" == "0" ]]; then
            cd $atlas_home; $pipenv run invoke group.create --name='GOJEK GoalBetter' --master-policy-number=P0000123 --sponsor-message='Some sponsor-message' --product='flep' --email='contact@gojek.com' --uen='GOKFLEP' 1>/dev/null 2>&1; cd - >/dev/null;
        fi

        psql_atlas_postgres_host "$query_master_policy_number_flip"
        if [[ "$result" == "0" ]]; then
            cd $atlas_home; $pipenv run invoke group.create --name='GOJEK GoalBetter' --master-policy-number=P0000124 --sponsor-message='Some sponsor-message' --product='flip' --email='contact@gojek.com' --uen='GOKFLIP' 1>/dev/null 2>&1; cd - >/dev/null;
        fi

        psql_atlas_postgres_host "$query_master_policy_number_pa"
        if [[ "$result" == "0" ]]; then
            cd $atlas_home; $pipenv run invoke group.create --name='GIS' --master-policy-number=P0000125 --sponsor-message='Some sponsor-message' --product='pa' --email='contact@gis.com' --uen='GISPA' 1>/dev/null 2>&1; cd - >/dev/null;
        fi

        psql_atlas_postgres_host "$query_master_policy_number_pa"
        if [[ "$result" == "0" ]]; then
            cd $atlas_home; $pipenv run invoke group.create --name='GIS' --master-policy-number=P0000135 --sponsor-message='Some sponsor-message' --product='gpac' --email='contact@gis.com' --uen='GISGPAC' 1>/dev/null 2>&1; cd - >/dev/null;
        fi
    else
        psql_atlas_postgres_host "$query_master_policy_number_flep"
        if [[ "$result" == "0" ]]; then
            echo "creating flep for group..."
            docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke group.create --name='GOJEK GoalBetter' --master-policy-number=P0000123 --sponsor-message='Some sponsor-message' --product='flep' --email='contact@gojek.com' --uen='GOKFLEP' 1>/dev/null 2>&1; cd - >/dev/null"
        fi

        psql_atlas_postgres_host "$query_master_policy_number_flip"
        if [[ "$result" == "0" ]]; then
            echo "creating flip for group..."
            docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke group.create --name='GOJEK GoalBetter' --master-policy-number=P0000124 --sponsor-message='Some sponsor-message' --product='flip' --email='contact@gojek.com' --uen='GOKFLIP' 1>/dev/null 2>&1; cd - >/dev/null"
        fi

        psql_atlas_postgres_host "$query_master_policy_number_pa"
        if [[ "$result" == "0" ]]; then
            echo "creating pa for group..."
            docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke group.create --name='GIS' --master-policy-number=P0000125 --sponsor-message='Some sponsor-message' --product='pa' --email='contact@gis.com' --uen='GISPA' 1>/dev/null 2>&1; cd - >/dev/null"
        fi

        psql_atlas_postgres_host "$query_master_policy_number_pa"
        if [[ "$result" == "0" ]]; then
            echo "creating gpac for group..."
            docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke group.create --name='GIS' --master-policy-number=P0000135 --sponsor-message='Some sponsor-message' --product='pa' --email='contact@gis.com' --uen='GISPA' 1>/dev/null 2>&1; cd - >/dev/null"
        fi
    echo "DONE"
    fi
}

function pipenv_run_invoke_sp_host() {
    if [[ $host == "release" ]]; then
        cd $atlas_home; log_sponsored_purchase=$($pipenv run invoke policy.sponsored-purchase --excel-file="$1/$2" 2>&1)
    else
        docker exec gc_atlas_tr bash -c "mkdir -p /tmp/testfiles"
        docker cp "$1/$2" "gc_atlas_tr:/tmp/$2"
        docker exec gc_atlas_tr bash -c "cd $atlas_home; $pipenv run invoke policy.sponsored-purchase --excel-file=/tmp/$2 1>/dev/null 2>&1; cd - >/dev/null"
    fi
}

function psql_atlas_postgres_host() {
    if [[ $host == "release" ]]; then
        if [[ $2 == "check_error_code" ]]; then
            psql -h localhost atlas -Ujarvis -t -c "$1" 1>/dev/null 2>&1; error_code=$?
        else
            result=`psql -h localhost atlas -Ujarvis -t -c "$1" | xargs`
        fi
    else
        if [[ $2 == "check_error_code" ]]; then
            docker exec gc_postgres_tr psql atlas -Upostgres -t -c "$1" 1>/dev/null 2>&1; error_code=$?
        else
            result=`docker exec gc_postgres_tr psql atlas -Upostgres -t -c "$1" | xargs`
        fi

    fi
}

function write_new_line(){
    echo $1 >> $2
}
# setup result stored here
setup_result='THERE IS AN ISSUE BEFORE SETUP'
# summary result stored here
summary_result='THERE IS AN ISSUE BEFORE START TESTING'

existing_data_log_file="$remote_folder/testfiles/existing_data_log"
import_data_log_file="$remote_folder/testfiles/import_data_log"
validation_data_log_file="$remote_folder/testfiles/validation_data_log"

validation_gpac_sg="testfiles/case00_1_auto_gpacs_sg_validation.xlsx"
validation_gpac_id="testfiles/case00_2_auto_gpacs_id_validation.xlsx"
validation_hcp_id="testfiles/case00_3_auto_hcps_id_validation.xlsx"

CASES=(
    "case01:testfiles/case01_auto_flep_expired_1month.xlsx"
    "case01_1:testfiles/case01_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case01_2:testfiles/case01_2_auto_flep_import_no_overlap_pass.xlsx"
    "case01_3:testfiles/case01_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case01_4:testfiles/case01_4_auto_flip_import_no_overlap_pass.xlsx"
    "case01_5:testfiles/case01_5_auto_pa_import_overlap_pass.xlsx"

    "case02:testfiles/case02_auto_flep_expired_3days.xlsx"
    "case02_1:testfiles/case02_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case02_2:testfiles/case02_2_auto_flep_import_no_overlap_pass.xlsx"
    "case02_3:testfiles/case02_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case02_4:testfiles/case02_4_auto_flip_import_no_overlap_pass.xlsx"
    "case02_5:testfiles/case02_5_auto_pa_import_overlap_pass.xlsx"

    "case03:testfiles/case03_auto_flep_inforce_endin_3days.xlsx"
    "case03_1:testfiles/case03_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case03_2:testfiles/case03_2_auto_flep_import_no_overlap_pass.xlsx"
    "case03_3:testfiles/case03_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case03_4:testfiles/case03_4_auto_flip_import_no_overlap_pass.xlsx"
    "case03_5:testfiles/case03_5_auto_pa_import_overlap_pass.xlsx"

    "case04:testfiles/case04_auto_flep_inforce_started_3days.xlsx"
    "case04_1:testfiles/case04_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case04_2:testfiles/case04_2_auto_flep_import_no_overlap_pass.xlsx"
    "case04_3:testfiles/case04_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case04_4:testfiles/case04_4_auto_flip_import_no_overlap_pass.xlsx"
    "case04_5:testfiles/case04_5_auto_pa_import_overlap_pass.xlsx"

    "case05:testfiles/case05_auto_flep_inforce_started_today.xlsx"
    "case05_1:testfiles/case05_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case05_2:testfiles/case05_2_auto_flep_import_no_overlap_pass.xlsx"
    "case05_3:testfiles/case05_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case05_4:testfiles/case05_4_auto_flip_import_no_overlap_pass.xlsx"
    "case05_5:testfiles/case05_5_auto_pa_import_overlap_pass.xlsx"

    "case06:testfiles/case06_auto_flep_paid_startnext_3days.xlsx"
    "case06_1:testfiles/case06_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case06_2:testfiles/case06_2_auto_flep_import_no_overlap_pass.xlsx"
    "case06_3:testfiles/case06_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case06_4:testfiles/case06_4_auto_flip_import_no_overlap_pass.xlsx"
    "case06_5:testfiles/case06_5_auto_pa_import_overlap_pass.xlsx"

    "case07:testfiles/case07_auto_flep_paid_startnext_1month.xlsx"
    "case07_1:testfiles/case07_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case07_2:testfiles/case07_2_auto_flep_import_no_overlap_pass.xlsx"
    "case07_3:testfiles/case07_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case07_4:testfiles/case07_4_auto_flip_import_no_overlap_pass.xlsx"
    "case07_5:testfiles/case07_5_auto_pa_import_overlap_pass.xlsx"

    "case08:testfiles/case08_auto_flip_expired_1month.xlsx"
    "case08_1:testfiles/case08_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case08_2:testfiles/case08_2_auto_flep_import_no_overlap_pass.xlsx"
    "case08_3:testfiles/case08_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case08_4:testfiles/case08_4_auto_flip_import_no_overlap_pass.xlsx"
    "case08_5:testfiles/case08_5_auto_pa_import_overlap_pass.xlsx"

    "case09:testfiles/case09_auto_flip_expired_3days.xlsx"
    "case09_1:testfiles/case09_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case09_2:testfiles/case09_2_auto_flep_import_no_overlap_pass.xlsx"
    "case09_3:testfiles/case09_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case09_4:testfiles/case09_4_auto_flip_import_no_overlap_pass.xlsx"
    "case09_5:testfiles/case09_5_auto_pa_import_overlap_pass.xlsx"

    "case10:testfiles/case10_auto_flip_inforce_endin_3days.xlsx"
    "case10_1:testfiles/case10_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case10_2:testfiles/case10_2_auto_flep_import_no_overlap_pass.xlsx"
    "case10_3:testfiles/case10_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case10_4:testfiles/case10_4_auto_flip_import_no_overlap_pass.xlsx"
    "case10_5:testfiles/case10_5_auto_pa_import_overlap_pass.xlsx"

    "case11:testfiles/case11_auto_flip_inforce_started_3days.xlsx"
    "case11_1:testfiles/case11_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case11_2:testfiles/case11_2_auto_flep_import_no_overlap_pass.xlsx"
    "case11_3:testfiles/case11_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case11_4:testfiles/case11_4_auto_flip_import_no_overlap_pass.xlsx"
    "case11_5:testfiles/case11_5_auto_pa_import_overlap_pass.xlsx"

    "case12:testfiles/case12_auto_flip_inforce_started_today.xlsx"
    "case12_1:testfiles/case12_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case12_2:testfiles/case12_2_auto_flep_import_no_overlap_pass.xlsx"
    "case12_3:testfiles/case12_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case12_4:testfiles/case12_4_auto_flip_import_no_overlap_pass.xlsx"
    "case12_5:testfiles/case12_5_auto_pa_import_overlap_pass.xlsx"

    "case13:testfiles/case13_auto_flip_paid_startnext_3days.xlsx"
    "case13_1:testfiles/case13_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case13_2:testfiles/case13_2_auto_flep_import_no_overlap_pass.xlsx"
    "case13_3:testfiles/case13_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case13_4:testfiles/case13_4_auto_flip_import_no_overlap_pass.xlsx"
    "case13_5:testfiles/case13_5_auto_pa_import_overlap_pass.xlsx"

    "case14:testfiles/case14_auto_flip_paid_startnext_1month.xlsx"
    "case14_1:testfiles/case14_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case14_2:testfiles/case14_2_auto_flep_import_no_overlap_pass.xlsx"
    "case14_3:testfiles/case14_3_auto_flip_import_overlap_1day_fail.xlsx"
    "case14_4:testfiles/case14_4_auto_flip_import_no_overlap_pass.xlsx"
    "case14_5:testfiles/case14_5_auto_pa_import_overlap_pass.xlsx"

    "case15:testfiles/case15_auto_pa_expired_1month.xlsx"
    "case15_1:testfiles/case15_1_auto_pa_import_overlap_fail.xlsx"
    "case15_2:testfiles/case15_2_auto_pa_import_no_overlap_pass.xlsx"
    "case15_3:testfiles/case15_3_auto_flep_import_overlap_1day_pass.xlsx"
    "case15_4:testfiles/case15_4_auto_flip_import_overlap_flep_1day_fail.xlsx"

    "case16:testfiles/case16_auto_pa_expired_3days.xlsx"
    "case16_1:testfiles/case16_1_auto_pa_import_overlap_fail.xlsx"
    "case16_2:testfiles/case16_2_auto_pa_import_no_overlap_pass.xlsx"
    "case16_3:testfiles/case16_3_auto_flip_import_overlap_1day_pass.xlsx"
    "case16_4:testfiles/case16_4_auto_flep_import_overlap_flip_1day_fail.xlsx"

    "case17:testfiles/case17_auto_pa_inforce_endin_3days.xlsx"
    "case17_1:testfiles/case17_1_auto_pa_import_overlap_fail.xlsx"
    "case17_2:testfiles/case17_2_auto_pa_import_no_overlap_pass.xlsx"
    "case17_3:testfiles/case17_3_auto_flep_import_overlap_1day_pass.xlsx"
    "case17_4:testfiles/case17_4_auto_flip_import_overlap_flep_1day_fail.xlsx"

    "case18:testfiles/case18_auto_pa_inforce_started_3days.xlsx"
    "case18_1:testfiles/case18_1_auto_pa_import_overlap_fail.xlsx"
    "case18_2:testfiles/case18_2_auto_pa_import_no_overlap_pass.xlsx"
    "case18_3:testfiles/case18_3_auto_flip_import_overlap_1day_pass.xlsx"
    "case18_4:testfiles/case18_4_auto_flep_import_overlap_flip_1day_fail.xlsx"

    "case19:testfiles/case19_auto_pa_inforce_started_today.xlsx"
    "case19_1:testfiles/case19_1_auto_pa_import_overlap_fail.xlsx"
    "case19_2:testfiles/case19_2_auto_pa_import_no_overlap_pass.xlsx"
    "case19_3:testfiles/case19_3_auto_flep_import_overlap_1day_pass.xlsx"
    "case19_4:testfiles/case19_4_auto_flip_import_overlap_flep_1day_fail.xlsx"

    "case20:testfiles/case20_auto_pa_paid_startnext_3days.xlsx"
    "case20_1:testfiles/case20_1_auto_pa_import_overlap_fail.xlsx"
    "case20_2:testfiles/case20_2_auto_pa_import_no_overlap_pass.xlsx"
    "case20_3:testfiles/case20_3_auto_flip_import_overlap_1day_pass.xlsx"
    "case20_4:testfiles/case20_4_auto_flep_import_overlap_flip_1day_fail.xlsx"

    "case21:testfiles/case21_auto_pa_paid_startnext_1month.xlsx"
    "case21_1:testfiles/case21_1_auto_pa_import_overlap_fail.xlsx"
    "case21_2:testfiles/case21_2_auto_pa_import_no_overlap_pass.xlsx"
    "case21_3:testfiles/case21_3_auto_flep_import_overlap_1day_pass.xlsx"
    "case21_4:testfiles/case21_4_auto_flip_import_overlap_flep_1day_fail.xlsx"

    "case22:testfiles/case22_auto_flep_expired_1month.xlsx"
    "case22X:testfiles/case22X_auto_flep_expired_1month_duplicate_temp.xlsx"
    "case22_1:testfiles/case22_1_auto_flep_import_overlap_1day_fail.xlsx"
    "case22_2:testfiles/case22_2_auto_flep_import_no_overlap_pass.xlsx"
    "case23:testfiles/case23_auto_flip_expired_1month.xlsx"
    "case23X:testfiles/case23X_auto_flip_expired_1month_duplicate_temp.xlsx"
    "case23_1:testfiles/case23_1_auto_flip_import_overlap_1day_fail.xlsx"
    "case23_2:testfiles/case23_2_auto_flip_import_no_overlap_pass.xlsx"
    "case24:testfiles/case24_auto_pa_expired_1month.xlsx"
    "case24X:testfiles/case24X_auto_pa_expired_1month_duplicate_temp.xlsx"
    "case24_1:testfiles/case24_1_auto_pa_import_overlap_1day_fail.xlsx"
    "case24_2:testfiles/case24_2_auto_pa_import_no_overlap_pass.xlsx"

    "case25:testfiles/case25_auto_gpac_expired_1month.xlsx"
    "case25_1:testfiles/case25_1_auto_gpac_import_overlap_fail.xlsx"
    "case25_2:testfiles/case25_2_auto_pa_import_overlap_fail.xlsx"
    "case25_3:testfiles/case25_3_auto_gpac_import_no_overlap_pass.xlsx"
    "case25_4:testfiles/case25_4_auto_flep_import_overlap_1day_pass.xlsx"

    "case26:testfiles/case26_auto_gpac_expired_3days.xlsx"
    "case26_1:testfiles/case26_1_auto_pa_import_overlap_fail.xlsx"
    "case26_2:testfiles/case26_2_auto_gpac_import_overlap_fail.xlsx"
    "case26_3:testfiles/case26_3_auto_pa_import_no_overlap_pass.xlsx"
    "case26_4:testfiles/case26_4_auto_flip_import_overlap_1day_pass.xlsx"

    "case27:testfiles/case27_auto_gpac_inforce_endin_3days.xlsx"
    "case27_1:testfiles/case27_1_auto_gpac_import_overlap_fail.xlsx"
    "case27_2:testfiles/case27_2_auto_pa_import_overlap_fail.xlsx"
    "case27_3:testfiles/case27_3_auto_gpac_import_no_overlap_pass.xlsx"
    "case27_4:testfiles/case27_4_auto_flep_import_overlap_1day_pass.xlsx"

    "case28:testfiles/case28_auto_gpac_inforce_started_3days.xlsx"
    "case28_1:testfiles/case28_1_auto_gpac_import_overlap_fail.xlsx"
    "case28_2:testfiles/case28_2_auto_pa_import_overlap_fail.xlsx"
    "case28_3:testfiles/case28_3_auto_pa_import_no_overlap_pass.xlsx"
    "case28_4:testfiles/case28_4_auto_flip_import_overlap_1day_pass.xlsx"

    "case29:testfiles/case29_auto_gpac_inforce_started_today.xlsx"
    "case29_1:testfiles/case29_1_auto_gpac_import_overlap_fail.xlsx"
    "case29_2:testfiles/case29_2_auto_pa_import_overlap_fail.xlsx"
    "case29_3:testfiles/case29_3_auto_gpac_import_no_overlap_pass.xlsx"
    "case29_4:testfiles/case29_4_auto_flep_import_overlap_1day_pass.xlsx"

    "case30:testfiles/case30_auto_gpac_paid_startnext_3days.xlsx"
    "case30_1:testfiles/case30_1_auto_gpac_import_overlap_fail.xlsx"
    "case30_2:testfiles/case30_2_auto_pa_import_overlap_fail.xlsx"
    "case30_3:testfiles/case30_3_auto_gpac_import_no_overlap_pass.xlsx"
    "case30_4:testfiles/case30_4_auto_flip_import_overlap_1day_pass.xlsx"

    "case31:testfiles/case31_auto_gpac_paid_startnext_1month.xlsx"
    "case31_1:testfiles/case31_1_auto_gpac_import_overlap_fail.xlsx"
    "case31_2:testfiles/case31_2_auto_pa_import_overlap_fail.xlsx"
    "case31_3:testfiles/case31_3_auto_pa_import_no_overlap_pass.xlsx"
    "case31_4:testfiles/case31_4_auto_flep_import_overlap_1day_pass.xlsx"
    )

# Color for PASS/FAIL
#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"

#normal=$(tput sgr0)
#red=$(tput setaf 1)
#green=$(tput setaf 2)
#yellow=$(tput setaf 3)
#blue=$(tput setaf 4)
#magenta=$(tput setaf 5)
#cyan=$(tput setaf 6)
#white=$(tput setaf 7)
#echo "This text is green"


setup_result="PASS"
summary_result="PASS"


# Verify if any master policy number of products
echo $(pipenv_run_invoke_create_group_host $host)

# Validation of GPAC SG
pipenv_run_invoke_sp_host $host $remote_folder $validation_gpac_sg
log1=$log_sponsored_purchase
# Validation of GPAC ID
pipenv_run_invoke_sp_host $host $remote_folder $validation_gpac_id
log2=$log_sponsored_purchase
# Validation of HCP ID
pipenv_run_invoke_sp_host $host $remote_folder $validation_hcp_id
log3=$log_sponsored_purchase


while read line; do
    caseid=$(echo $line | cut -d':' -f 1)
    if [[ $caseid == *"case00"* ]]; then
        printf 'Validation for '
        upper_caseid=`echo $caseid | tr '[:lower:]' '[:upper:]'`
        printf %s "$upper_caseid" ' - '

        case_data=($(echo $line | tr ":" "\n"))
        data=($(echo ${case_data[1]} | tr "," "\n"))
        product=${data[0]}
        nricfin=${data[1]}
        policy_start=${data[2]}
        #status=${data[3]}

        q="
        SELECT count(*) FROM policies WHERE nricfin='"$nricfin"';
        "
        psql_atlas_postgres_host "$q"

        if [[ "$caseid" == *"case00_1"* ]]; then
            printf "GPAC SGP - "
            passfail=`if [[ "$result" == "0" ]]; then printf "PASS"; else printf "FAIL"; fi`; echo $passfail
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL"
                append_log $caseid "$log1"
            fi
        elif [[ $caseid == *"case00_2"* ]]; then
            printf "GPAC IDN - "
            passfail=`if [[ "$result" == "0" ]]; then printf "PASS"; else printf "FAIL"; fi`; echo $passfail
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL"
                append_log $caseid "$log2"
            fi
        elif [[ $caseid == *"case00_3"* ]]; then
            printf "HCP IDN - "
            if [[ $caseid == "case00_3_27" ]]; then
                passfail=`if [[ "$result" == "1" ]]; then printf "PASS"; else printf "FAIL"; fi`; echo $passfail
            else
                passfail=`if [[ "$result" == "0" ]]; then printf "PASS"; else printf "FAIL"; fi`; echo $passfail
            fi
            if [[ "$passfail" == "FAIL" ]]; then
                summary_result="FAIL"
                append_log $caseid "$log3"
            fi
        fi
    fi
done < $validation_data_log_file

echo "
CREATE EXISTING DATA"

GC2365=("case22" "case23" "case24")

for i in "${CASES[@]}"
do
    KEY="${i%%:*}"
    VALUE="${i##*:}"
    if [[ $KEY != *"_"* ]]; then
        printf 'Create existing data for '
        caseid=`echo $KEY | tr '[:lower:]' '[:upper:]'`
        printf %s "$caseid" ' - '

        pipenv_run_invoke_sp_host $remote_folder $VALUE
        # Read data from log file
        i=0
        while read line; do
        # Reading each line
        i=$((i+1))
        if [[ $(echo $line | cut -d':' -f 1) == $KEY ]]; then
            case_data=($(echo $line | tr ":" "\n"))
            data=($(echo ${case_data[1]} | tr "," "\n"))
            product=${data[0]}
            nricfin=${data[1]}
            policy_start=${data[2]}
            status=${data[3]}

            # Verify data in db
            q="
            SELECT count(*) FROM policies WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"';
            "
            psql_atlas_postgres_host "$q"
            #result=`psql atlas -t -c "$q" | xargs`
            passfail=`if [[ "$result" == "1" ]]; then echo "PASS"; else echo "FAIL"; fi`; echo $passfail
            if [[ $passfail == "FAIL" ]]; then
                setup_result="FAIL"
                append_log $caseid $log_sponsored_purchase
            fi

            # GC-2365
            for j in "${GC2365[@]}"
            do
                if [[ $KEY == $j ]]; then
                    q_policy_end="
                    SELECT policy_end FROM policies WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"' and status='"$status"';
                    "
                    psql_atlas_postgres_host "$q_policy_end"
                    last_policy_end=$result
                    last_policy_start=$policy_start
                fi
            done

            q_policy_number="
            SELECT policy_number FROM policies WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"' and status='"$status"';
            "
            psql_atlas_postgres_host "$q_policy_number"
            policy_number=$result
            write_new_line "$policy_number,$product,$nricfin,$policy_start,$status" "$remote_folder/testfiles/email_existing_data"

            if [[ $KEY == *"X"* ]]; then
                # Update data in db
                q="
                UPDATE policies SET status='in_force', policy_start='"$last_policy_start"', policy_end='"$last_policy_end"' WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"';
                "
                psql_atlas_postgres_host "$q" "check_error_code"
                #psql atlas -t -c "$q"; 1>/dev/null 2>&1; error_code=$?
                passfail=`if [[ "$error_code" == "0" ]]; then echo "PASS"; else echo "FAIL"; fi`; echo $passfail
                if [[ $passfail == "FAIL" ]]; then
                    setup_result="FAIL"
                    append_log $caseid "$log_sponsored_purchase"
                fi
            fi

            break
        fi
        done < $existing_data_log_file

    fi
done


echo '
START TESTING'

for i in "${CASES[@]}"
do
    KEY="${i%%:*}"
    VALUE="${i##*:}"
    if [[ $KEY == *"_"* ]]; then
        pipenv_run_invoke_sp_host $remote_folder $VALUE
        # Read data from log file
        i=0
        while read line; do
            # Reading each line
            caseid=$(echo $line | cut -d':' -f 1)
            case_data=($(echo $line | cut -d':' -f 2))
            if [[ $caseid != *"case00"* && $caseid == $KEY ]]; then
                printf 'Execute test for '
                upper_caseid=`echo $caseid | tr '[:lower:]' '[:upper:]'`
                printf %s "$upper_caseid" ' - '

                i=$((i+1))
                data=($(echo $case_data | tr "," "\n"))
                product=${data[0]}
                nricfin=${data[1]}
                policy_start=${data[2]}
                status=${data[3]}
                expected=${data[4]}
                expected_result=0
                if [[ $expected == "PASS" ]]; then expected_result=1; fi
                expected_msg=`if [[ "$expected_result" == "0" ]]; then printf "Expected result: DO NOT IMPORT -> "; else printf "Expected result:        IMPORT -> "; fi`; printf "$expected_msg"

                q_policy_number="
                SELECT policy_number FROM policies WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"' and status='"$status"';
                "
                psql_atlas_postgres_host "$q_policy_number"

                policy_number=$result
                write_new_line "$policy_number,$product,$nricfin,$policy_start,$status" "$remote_folder/testfiles/email_import_data"

                # Verify data in db
                q="
                SELECT count(*) FROM policies WHERE product='"$product"' and nricfin='"$nricfin"' and policy_start='"$policy_start"' and status='"$status"';
                "
                #result=`psql atlas -t -c "$q" | xargs`
                psql_atlas_postgres_host "$q"
                passfail=`if [[ "$result" == $expected_result ]]; then echo "PASS"; else echo "FAIL"; fi`
                if [[ $KEY == *"case21"* || $KEY == *"case22"* || $KEY == *"case23"* ]]; then
                    if [[ $passfail == "FAIL" ]]; then
                        echo "https://gigacover.atlassian.net/browse/GC-2365";
                    else echo $passfail; fi
                elif [[ $KEY == "case25_4" ]]; then
                    if [[ $passfail == "FAIL" ]]; then
                        echo "https://gigacover.atlassian.net/browse/GC-3173";
                    else echo $passfail; fi
                else
                    echo $passfail
                fi
                if [[ "$passfail" == "FAIL" ]]; then
                    summary_result="FAIL"
                    append_log $caseid "$log_sponsored_purchase"
                fi
                break
            fi
        done < $import_data_log_file
    fi
done

# SUMMARY
if [[ "$setup_result" == "FAIL" ]]; then
echo '

SPONSORED PURCHASE: SETUP FAIL'
elif [[ "$summary_result" == "FAIL" ]]; then
echo '

SPONSORED PURCHASE: FAIL'
elif [[ "$setup_result" == "PASS" && "$summary_result" == "PASS" ]]; then
echo '

SPONSORED PURCHASE: PASS'
else
echo "

SPONSORED PURCHASE: $summary_result"
fi

