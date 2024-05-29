#!/usr/bin/env bash

seleniumContainers="docker ps -qa
                              -f name=chrome
"
sh="docker stop $($seleniumContainers)"
echo "$sh"
eval $sh

docker rm $($seleniumContainers) #remove all when needed
