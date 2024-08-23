#!/bin/bash
SH=$(cd `dirname $BASH_SOURCE` && pwd)
AH=$(cd "$SH/../../" && pwd)

set -a  # broadcast defined var as envvar to subroutine ON
    source "$AH/.env"  # load app envvar  eg db connection DB_xx xx=port/user/pasw/name
    [ $? != 0 ] && (echo  "ERROR cannot load $AH/.env"; kill $$)

        [ -z $CONTAINER_PROJECT ] && (echo "Envvar CONTAINER_PROJECT is required"; kill $$)

        cd $SH
        set -x  # autoprint command when run
            docker-compose \
                -p $CONTAINER_PROJECT \
                -f "$SH/docker-compose.yml" \
                down -t0
