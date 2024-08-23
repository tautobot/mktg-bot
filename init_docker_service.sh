#!/bin/bash
SH=$(cd `dirname $BASH_SOURCE` && pwd)

echo $SH

# load envvar
source .env

# build requirement package
pipenv install
pipenv lock --requirements > requirements.txt
pipenv requirements > requirements.txt

sudo apt-get update -y; sudo apt-get upgrade -y

# build docker

	echo; echo "--> BUILD the base docker image"
	docker build --build-arg APP_PORT=$APP_PORT --no-cache --file "./Dockerfile" -t $BASE_IMAGE_NAME .

# delete env.runtime
rm -rf requirements.txt
rm -rf ./script/app/.container-volume
rm -rf ./migrations

docker network create proxy

# up all services
/bin/bash ./script/app/up.sh
