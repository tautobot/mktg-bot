#!/bin/bash
run() {
    local SH=$(cd `dirname $BASH_SOURCE` && pwd)
    local AH=$(cd "$SH/../../" && pwd)

    echo $SH;
    echo $AH;

    set -a  # broadcast defined var as envvar to subroutine ON
        source "$AH/.env"  # load app envvar  eg db connection DB_xx xx=port/user/pasw/name
        [ $? != 0 ] && (echo  "ERROR cannot load $AH/.env"; kill $$)

            [ -z $CONTAINER_PROJECT ] && (echo "Envvar CONTAINER_PROJECT is required"; kill $$)


            cd $SH

                docker-compose  -p $CONTAINER_PROJECT  -f "$SH/docker-compose.yml"  up -d --build
                    echo
                    docker ps --format '{{.Names}} {{.Ports}} {{.Networks}}' | grep -E "$DB_CONTAINER_NAME|$PUBLIC_DB_PORT|$DOCKER_NETWORK" --color=always

}
    run
