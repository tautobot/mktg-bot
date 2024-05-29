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
      env_postgres=$SSH;               env_atlas=$SSH;            user="jarvis";       cp="scp " ;      atlas=$user_at_host ;    pipenv='/home/trang/.pyenv/shims/pipenv'
elif [[ "$environment" == 'docker' ]]; then
      env_postgres=$docker_postgres;   env_atlas=$docker_atlas ;  user="postgres";     cp="docker cp "; atlas=$container_atlas ; pipenv='/usr/local/bin/pipenv'
else
      echo 'can not find environment in config_local file'
      exit
fi

  $cp "$SCRIPT_HOME/01.onboard_worker.sh_run_on_remote.sh" $atlas:"$WORKING_DIR_FIXTURE/01.onboard_worker.sh_run_on_remote.sh"

  $cp "$ROOT/aQA/fixtures/benefits_template_no_nricfin.xlsx" $atlas:"$WORKING_DIR_FIXTURE/benefits.xlsx"

  $env_atlas "$WORKING_DIR_FIXTURE/01.onboard_worker.sh_run_on_remote.sh $pipenv"

  $env_postgres "psql -U $user atlas -h localhost -c 'update users set \"refreshToken\"='123' where \"group\"='\'test_aqa_benefits\''; ' "
