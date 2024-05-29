#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../.."; ROOT=$(cd "$ROOT" && pwd)

container_atlas="gc_atlas_tt"
container_postgres="gc_postgres_tt"

docker_postgres="docker exec -i $container_postgres bash -c"
docker_atlas="docker exec -i $container_atlas bash -ic"

source "$ROOT/config_local.py";

if [[ "$environment" == 'local' ]];
  then ip=$ip_release
  else ip=$ip_docker
fi

user_at_host="trang@$ip"
SSH="ssh $user_at_host"

if [[ "$environment" == 'local' ]]; then
      env_postgres=$SSH;              user="jarvis";
elif [[ "$environment" == 'docker' ]]; then
      env_postgres=$docker_postgres;  user="postgres";
else
      echo 'can not find environment in config_local file'
      exit
fi

cd $ROOT; export PYTHONPATH=$PYTHONPATH:$PWD; pipenv sync


printf '\n=== Flep Sponsor Purchase ===\n'
  echo "--> Create fixture"
  python -c 'from testcases.lib.generic import * ; generate_date();';
  $SCRIPT_HOME/00.create_group.sh &>$WORKING_DIR_FIXTURE/create_group.log
  echo "DONE"

  echo "--> Sponsor Purchase";
  $SCRIPT_HOME/01.create_users.sh &>$WORKING_DIR_FIXTURE/sponsor_purchase.log
  echo "DONE"

  echo "--> Claim and verify past claim"
  info=$(pytest -v -s $SCRIPT_HOME/test_flep.py 2>&1)
  result=$(echo "$info" | tail -n1 | sed 's/[=]//g')
    if [[ "$result" == *"failed"* ]]; then
      echo "$info" > "$WORKING_DIR_LOGS/Claim_and_verify_past_claim.txt"
  fi
  printf "$result \n";
