#!/usr/bin/env bash
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
      env_postgres=$SSH;               env_atlas=$SSH;            user="jarvis";       cp="scp " ;        atlas=$user_at_host ;    pipenv='/home/trang/.pyenv/shims/pipenv'
elif [[ "$environment" == 'docker' ]]; then
      env_postgres=$docker_postgres;   env_atlas=$docker_atlas ;  user="postgres";     cp="docker cp ";   atlas=$container_atlas ; pipenv='/usr/local/bin/pipenv'
else
      echo 'can not find environment in config_local file'
      exit
fi

  $env_atlas "mkdir $WORKING_DIR_FIXTURE"

  # delete from insurer_sum_assured table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from insurer_sum_assured where policy_id in (select id from policies where sponsor = '\'test_aqa_hcp\'');' "
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from insurer_sum_assured where schedule_id in (select id from files where nricfin in (select nricfin from users where \"group\" = '\'test_aqa_hcp\''));' "

  # delete from transactions table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from transactions where bill_id in (select id from bills where email in (select email from policies where sponsor = '\'test_aqa_hcp\''));' "

  # delete from bills table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from bills where email in (select email from policies where sponsor = '\'test_aqa_hcp\'');' "

  # delete from policies table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from policies where sponsor = '\'test_aqa_hcp\'';' "

  # delete from files table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from files where nricfin in (select nricfin from users where \"group\" = '\'test_aqa_hcp\'');' "

  # delete from transactions table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from transactions where bill_id in (select id from bills where bills.email in (select email from policies where sponsor = '\'test_aqa_hcp\''));' "

  # delete from policies table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from policies where sponsor = '\'test_aqa_hcp\'';' "

  # delete from policies self-bought user
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from policies where email = '\'s4984534j@gigacover.com\'';' "

  # delete from settings table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from settings where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_hcp\''); ' "

  # delete from files table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from files where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_hcp\''); ' "

  # delete from claims table
  $env_postgres "psql -U $user atlas -h localhost -c 'delete from claims where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_hcp\''); ' "

  # delete from mobiles table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from mobiles where nricfin in ( select nricfin from users where \"group\"='\'test_aqa_hcp\''); '"  >/dev/null 2>&1

  # delete from account table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from accounts where user_id in ( select id from users where \"group\"='\'test_aqa_hcp\''); '"  >/dev/null 2>&1

  # delete from users table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from users where \"group\"='\'test_aqa_hcp\''; '"

  # delete from master_policy_numbers table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from master_policy_numbers where sponsor = '\'test_aqa_hcp\'';'"

  # delete from groups table
  $env_postgres "psql -U $user atlas -h localhost  -c 'delete from groups where name='\'test_aqa_hcp\''; '"

  # copy file create group to remote
  $cp "$SCRIPT_HOME/00.create_group_run_on_remote.sh" $atlas:"$WORKING_DIR_FIXTURE/00.create_group_run_on_remote.sh"

  # copy file create user to remote
  $cp "$SCRIPT_HOME/00.create_user.sh_run_on_remote.sh" $atlas:"$WORKING_DIR_FIXTURE/00.create_user.sh_run_on_remote.sh"

  # copy excel template to remote
  $cp "$ROOT/aQA/fixtures/hcp_template.xlsx" $atlas:"$WORKING_DIR_FIXTURE/hcp.xlsx"
  $cp "$ROOT/aQA/fixtures/hcp_nonric_template.xlsx" $atlas:"$WORKING_DIR_FIXTURE/hcp_nonric_template.xlsx"

  # copy variable file to remote
  $cp "$ROOT/aQA/fixtures/variable.xlsx" $atlas:"$WORKING_DIR_FIXTURE/variable.xlsx"

  # copy product template file to remote
  $cp "$ROOT/aQA/fixtures/template.xlsx" $atlas:"$WORKING_DIR_FIXTURE/template.xlsx"

  # create group
  $env_atlas "$WORKING_DIR_FIXTURE/00.create_group_run_on_remote.sh $pipenv"

  # create user
  $env_atlas "$WORKING_DIR_FIXTURE/00.create_user.sh_run_on_remote.sh $pipenv"
  $env_postgres "psql -U $user atlas -h localhost -c 'update users set \"refreshToken\"='123' where \"group\"='\'test_aqa_hcp\''; ' "
