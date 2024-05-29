#!/bin/bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

docker_postgres="docker exec -i $container_postgres bash -c"
docker_atlas="docker exec -i $container_atlas bash -ic"

if [[ "$environment" == 'local' ]];
  then ip=$ip_release
  else ip=$ip_docker
fi

user_at_host="trang@$ip"
SSH="ssh $user_at_host"


if [[ "$environment" == 'local' ]]; then
      env_postgres=$SSH;               env_atlas=$SSH;            user="jarvis";       cp="scp " ;       url="auth-release.gigacover.com" ; atlas=$user_at_host ;    pipenv='/home/trang/.pyenv/shims/pipenv'
elif [[ "$environment" == 'docker' ]]; then
      env_postgres=$docker_postgres;   env_atlas=$docker_atlas ;  user="postgres";     cp="docker cp ";  url="http://$ip:21262"             ; atlas=$container_atlas ; pipenv='/usr/local/bin/pipenv'
else
      echo 'can not find environment in config_local file'
      exit
fi

  $env_atlas "mkdir $WORKING_DIR_FIXTURE"

  # delete from transaction table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from transactions where account_id in ( select id from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances\'')); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from transactions where account_id in ( select id from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\'')); '"

  # delete from orders table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from orders where to_account_id in ( select id from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances\'')); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from orders where to_account_id in ( select id from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\'')); '"

  # delete from user_accounts table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from account table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

 # delete from advance_statuses table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from advance_statuses where advance_id in ( select id from advances where nricfin in (select nricfin from users where \"group\"='\'test_aqa_advances\'')); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from advance_statuses where advance_id in ( select id from advances where nricfin in (select nricfin from users where \"group\"='\'test_aqa_advances_tier\'')); '"

  # delete from mobiles table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from mobiles where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from mobiles where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from advances table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from advances where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from advances where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from files table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from files where id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from files where id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from orders table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from orders where user_id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from orders where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from notifications table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from notifications where user_id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from notifications where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from user_change_logs table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_change_logs where on_user in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_change_logs where on_user in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from user_product_scores table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_product_scores where user_id in ( select id from users where \"group\"='\'test_aqa_advances\''); '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from user_product_scores where user_id in ( select id from users where \"group\"='\'test_aqa_advances_tier\''); '"

  # delete from users table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from users where \"group\"='\'test_aqa_advances\''; '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from users where \"group\"='\'test_aqa_advances_tier\''; '"

  # delete from master_policy_numbers table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from master_policy_numbers where sponsor = '\'test_aqa_advances\'';'"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from master_policy_numbers where sponsor = '\'test_aqa_advances_tier\'';'"

  # delete from group_categories table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from group_categories where group_id in (select id from groups where name = '\'test_aqa_advances\'');'"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from group_categories where group_id in (select id from groups where name = '\'test_aqa_advances_tier\'');'"

  # delete from advance_tiers table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from advance_tiers where group_id in (select id from groups where name = '\'test_aqa_advances_tier\'');'"

  # delete from groups table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from groups where name='\'test_aqa_advances\''; '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from groups where name='\'test_aqa_advances_tier\''; '"

  # copy file create group to remote
  $cp "$SCRIPT_HOME/00.create_group_run_on_remote.sh" $atlas:"$WORKING_DIR_FIXTURE/00.create_group_run_on_remote.sh"

  # copy file create user to remote
  $cp "$SCRIPT_HOME/00.create_user.sh_run_on_remote.sh" $atlas:"$WORKING_DIR_FIXTURE/00.create_user.sh_run_on_remote.sh"

  # copy excel template to remote
  $cp "$ROOT/aQA/fixtures/advances_template.xlsx" $atlas:"$WORKING_DIR_FIXTURE/advances.xlsx"

  # copy tier template to remote
  $cp "$ROOT/aQA/fixtures/advances_tier_group.xlsx" $atlas:"$WORKING_DIR_FIXTURE/tier_group.xlsx"

  # create group
  $env_atlas "$WORKING_DIR_FIXTURE/00.create_group_run_on_remote.sh $pipenv"

  $env_postgres "psql -U $user atlas -h localhost  -c 'update groups set max_percentage_salary = 60, requests_allowed = 3, payroll_salary_day = 31, cutoff_days=0, advances_processing_fee=20000, auto_approval=True where name='\'test_aqa_advances\''; '"
  $env_postgres "psql -U $user atlas -h localhost  -c 'update groups set max_percentage_salary = 60, requests_allowed = 3, payroll_salary_day = 31, cutoff_days=0, advances_processing_fee=20000, auto_approval=True, admin_fee_type='\'tier\'' where name='\'test_aqa_advances_tier\''; '"


  echo "--> Change password of Group owner"
  link=$($env_atlas "cat /tmp/aqa/owner_advance.log | grep $url | tail -2 | head -n1" 2>&1 )
  u=$(echo "$link" | cut -d '"' -f2)
  curl -i -X POST ""$u""  -H 'Content-Type: application/json'  -d '{"password":"Test1234", "confirmPassword":"Test1234"}' 2>&1 | grep successfully | cut -d '>' -f28 | cut -d '<' -f1

  link1=$($env_atlas "cat /tmp/aqa/owner_advance_tier.log | grep $url | tail -2 | head -n1" 2>&1 )
  u1=$(echo "$link1" | cut -d '"' -f2)
  curl -i -X POST ""$u1""  -H 'Content-Type: application/json'  -d '{"password":"Test1234", "confirmPassword":"Test1234"}' 2>&1 | grep successfully | cut -d '>' -f28 | cut -d '<' -f1

  # create user
  $env_atlas "$WORKING_DIR_FIXTURE/00.create_user.sh_run_on_remote.sh $pipenv"
  $env_postgres "psql -U $user atlas -h localhost -c 'update users set \"refreshToken\"='123' where \"group\"='\'test_aqa_advances\''; ' "
  $env_postgres "psql -U $user atlas -h localhost -c 'update users set \"refreshToken\"='123' where \"group\"='\'test_aqa_advances_tier\''; ' "
