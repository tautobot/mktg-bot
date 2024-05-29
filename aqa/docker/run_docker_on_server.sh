#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../"; a=$(cd "$a" && pwd); APP_HOME=$a; ROOT="$APP_HOME/../../"; ROOT=$(cd "$ROOT" && pwd)

source "$ROOT/config_local.py";

export GC_INSTANCE_ID='tt'; export PUBLISHED_HOST=$ip_docker;
#cd /opt/gigacover/devops && git pull && git status | head -n1 && git log --oneline -n2

CURRENT_USER=`whoami`;
source /home/$CURRENT_USER/.nvm/nvm.sh;
GC_INSTANCE_ID=$GC_INSTANCE_ID PUBLISHED_HOST=$PUBLISHED_HOST
    REMOVE_CURRENT_BUILD=1  \
    SKIP_GIT_PULL=0 \
    SKIP_DB_RESET=1 \
    ONLY_CONTAINERS="" \
    GIT_URI=bitbucket.org:gigacover \
    ATLAS_GIT_BRANCH=develop \
    SENTINEL_GIT_BRANCH=develop \
    VENTA_GIT_BRANCH=master \
    ESSENTIALS_GIT_BRANCH=master \
    /opt/gigacover/devops/gc-staging/up.sh | tee /home/$CURRENT_USER/gcsu$GC_INSTANCE_ID
